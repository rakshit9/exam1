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

if __name__ == '__main__':
    app.run(debug=True)

