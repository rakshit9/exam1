from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['IMAGE_FOLDER'] = 'static'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
