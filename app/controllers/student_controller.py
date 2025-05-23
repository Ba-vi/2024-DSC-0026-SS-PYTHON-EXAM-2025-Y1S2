from app.extensions import db
from app.models.student_model import Student
from flask import Blueprint, jsonify, request
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR



#registering a student
students = Blueprint("students", __name__, url_prefix='/api/v1/students')
@students.route("/register", methods=['POST'])
def register_student():

    # storing the student details.
    data = request.get_json()
    id = data.get("id")
    name = data.get('name')
    email = data.get('email')
    program_id = data.get('program_id')
    contact = data.get('contact')
  
    # validating the student details by checking if all the attributes are provided.
    if not name or not email or not program_id or not contact or not id:
        return jsonify({"error": "All fields are required"}),HTTP_400_BAD_REQUEST

    # check for duplicate email or id
    if Student.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), HTTP_409_CONFLICT
    
    if Student.query.get(id):
        return jsonify({"error": "Student ID already exists"}), HTTP_409_CONFLICT

    try:
        # creating a new student
        new_student = Student(
            id=id,
            name=name,
            email=email, 
            program_id=program_id, 
            contact=contact
        )
        # adding a new student to the database.
        db.session.add(new_student)
        db.session.commit()

        # returning the response(student details).
        return jsonify({
            "message": "Student created successfully",
            "student": {
                "id": new_student.id,
                "name": new_student.name,
                "email": new_student.email,
                "contact": new_student.contact,
                "program_id": new_student.program_id
            }}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

#getting all student details
@students.route('/students', methods=['GET'])
def get_all_students():

    try:
        students = Student.query.all()
        return jsonify({
            "students": [
                {
                    "id": student.id,
                    "name": student.name,
                    "email": student.email,
                    "contact": student.contact,
                    "program_id": student.program_id
                } 
            for student in students
        ]}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


#deleting  a student by id.
@students.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), HTTP_404_NOT_FOUND

    # removing the student from the database.
    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), HTTP_200_OK