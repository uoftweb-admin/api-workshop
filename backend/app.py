from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# SQLite Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

# Ensure tables are created when the app starts
with app.app_context():
    db.create_all()

### CREATE a course
@app.route('/courses', methods=['POST'])
def add_course():
    return

### READ a single course
@app.route('/courses/<course_code>', methods=['GET'])
def get_course(course_code):
    return


### READ all courses
@app.route('/courses', methods=['GET'])
def get_all_courses():
    return


### UPDATE a course
@app.route('/courses/<course_code>', methods=['PUT'])
def update_course(course_code):
    return

### DELETE a course
@app.route('/courses/<course_code>', methods=['DELETE'])
def delete_course(course_code):
    return

### 🌍 Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)