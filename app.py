from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['IMAGE_FOLDER'] = 'static'


@app.route('/', methods=['GET', 'POST'])
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sinong.jpg')
    return render_template("index.html", user_image = full_filename)

@app.route('/search_user', methods=['GET', 'POST'])
def search():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sinong.jpg')
    if request.method == 'POST':
        name = request.form['name']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'q1x.csv')
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'].lower() == name.lower():
                
                    if row['pic']:
                        image_path = os.path.join(app.config['IMAGE_FOLDER'], row['pic'])
                        print(f"Checking if {image_path} exists: {os.path.exists(image_path)}")  # Debug
                        if os.path.exists(image_path):
                            image_url = url_for('static', filename=row['pic'])
                            print(f"Image URL: {image_url}")  # Debug
   
                            return render_template('display_user_info.html',name=row["name"],cost=row["cost"],descript=row["descript"], image_url=image_url,user_image = full_filename)
                        else:
                              return render_template('display_user_info.html',name=row["name"],cost=row["cost"],descript=row["descript"],user_image = full_filename)
                    
                    return render_template('error.html', message="Image file is missing.")
            return render_template('error.html', message="No such name found.")
    return render_template('search_user.html',user_image = full_filename)




@app.route('/display_user_range_info', methods=['GET', 'POST'])
def get_display_user_info():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sinong.jpg')
    if request.method == 'POST':
        range1 = int(request.form.get('range1') or 0)
        range2 = int(request.form.get('range2') or 0)
        id_range1 = int(request.form.get('id_range1') or 0)
        id_range2 = int(request.form.get('id_range2') or 0)
       
        students = []
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # gets the directory of the current file
        file_path = os.path.join(BASE_DIR, 'static', 'q1x.csv')  # constructs the path to the csv file
        with open(file_path) as file:
            csv_reader = csv.DictReader(file)
            for r in csv_reader:
                grade_check = r['cost'].strip().isdigit() and range1 <= int(r['cost']) <= range2 if range1 or range2 else True
                if grade_check:
    # name,cost,pic,descript
                    student = dict()
                    student['name'] = r['name']
                    student['cost'] = r['cost']
                    student['descript'] = r['descript']
                    if r['pic'].strip():
                        student['pic'] = 'static/' + r['pic']
                    else:
                        student['pic'] = 'static/no_picture.png'
                    students.append(student)
        if students:
            return render_template('display_user_info.html', students=students, user_image = full_filename)
        else:
            return render_template('display_user_info.html', error="No students found in this grade range", user_image = full_filename)
    return render_template('search_range.html',user_image = full_filename)



@app.route('/update_entry', methods=['GET','POST'])
def update_entry():
    if request.method == 'POST':
        name_to_update = request.form['name'].strip().lower()  # Name from the form
        descript = request.form['descript'].strip()
        print(name_to_update)

        # Collect field updates from the form
        updates = {
            'descript': request.form['descript'].strip(),
            # 'Salary': request.form['salary'].strip(),
            # 'Grade': request.form['grade'].strip(),
            # 'Room': request.form['room'].strip(),
            # 'Telnum': request.form['telnum'].strip(),
            # 'Picture': request.form['picture'].strip(),
            # 'Keywords': request.form['keywords'].strip()
        }

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'q1x.csv')
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_q1x.csv')
        updated = False

        try:
            with open(filepath, 'r', newline='') as csvfile, open(temp_file_path, 'w', newline='') as tempfile:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row['name'].strip().lower() == name_to_update:
                        print("=========="+row["name"])
                        row['descript'] = descript
                        # for field, value in updates.items():
                        #     if value:  # Only update fields that have a new value provided
                        #         row[field] = value
                        updated = True
                    writer.writerow(row)

            os.replace(temp_file_path, filepath)
            return f'Entry updated successfully for {name_to_update.title()}!' if updated else f'No entry found for {name_to_update.title()}.'
        except Exception as e:
            return str(e), 500
    return render_template('update_entry.html')



@app.route('/remove_entry', methods=['GET', 'POST'])
def remove_entry():
    full_filename = os.path.join(app.config['IMAGE_FOLDER'], 'sinong.jpg')
    if request.method == 'POST':
        name_to_remove = request.form['name'].strip().lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'q1x.csv')
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_q1x.csv')

        try:
            with open(filepath, 'r', newline='') as csvfile, open(temp_file_path, 'w', newline='') as tempfile:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                print("Fieldnames:", fieldnames)  # Debugging line

                writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
                writer.writeheader()

                removed = False
                for row in reader:
                    print("Current row:", row)  # Debugging line
                    if row['name'] != name_to_remove:  # Ensure 'Name' matches CSV header
                        print("gg")
                        writer.writerow(row)
                    else:
                        print("working")
                        removed = True
            print(removed,"astksdfasdfas")
            if removed:
                os.replace(temp_file_path, filepath)
                return f'{name_to_remove.title()} removed successfully!'
            else:
                return f'No entry found for {name_to_remove.title()}.'
        except Exception as e:
            print("Error:", str(e))  # More detailed error logging
            return str(e), 500

    return render_template('remove_entry.html', user_image=full_filename)




if __name__ == '__main__':
    app.run(debug=True)

