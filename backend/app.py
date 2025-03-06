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
    data = request.json
    if not data.get("course_code"):
        return jsonify({"error": "Course code is required"}), 400

    new_course = Course(
        course_code=data["course_code"],
        year=data["year"],
        semester=data["semester"],
        instructor=data["instructor"],
        name=data["name"]
    )

    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course added successfully", "course": data}), 201

### READ all courses
@app.route('/courses', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    return jsonify([{
        "course_code": course.course_code,
        "year": course.year,
        "semester": course.semester,
        "instructor": course.instructor,
        "name": course.name
    } for course in courses]), 200

### READ a single course
@app.route('/courses/<course_code>', methods=['GET'])
def get_course(course_code):
    course = Course.query.filter_by(course_code=course_code).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "course_code": course.course_code,
        "year": course.year,
        "semester": course.semester,
        "instructor": course.instructor,
        "name": course.name
    }), 200

### UPDATE a course
@app.route('/courses/<course_code>', methods=['PUT'])
def update_course(course_code):
    course = Course.query.filter_by(course_code=course_code).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.json
    course.year = data.get("year", course.year)
    course.semester = data.get("semester", course.semester)
    course.instructor = data.get("instructor", course.instructor)
    course.name = data.get("name", course.name)

    db.session.commit()
    return jsonify({"message": "Course updated successfully"}), 200

### DELETE a course
@app.route('/courses/<course_code>', methods=['DELETE'])
def delete_course(course_code):
    course = Course.query.filter_by(course_code=course_code).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": f"Course {course_code} deleted successfully"}), 200

### 🌍 Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)