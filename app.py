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



if __name__ == '__main__':
    app.run(debug=True)

