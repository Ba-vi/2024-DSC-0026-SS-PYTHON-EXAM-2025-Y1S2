from app.extensions import db
from app.models.course_model import Course
from flask import Blueprint, jsonify, request
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR

#registering a course
courses = Blueprint("courses", __name__, url_prefix='/api/v1/courses')
@courses.route("/register", methods=['POST'])
def register_course():
    #storing the course details
    data = request.get_json()
    id=data.get("id")
    name = data.get("name")
    program_id = data.get("program_id")

    if not name or not program_id or not id:
        return jsonify({"error": "All fields are required."}), HTTP_400_BAD_REQUEST
    # registering new course details
    new_course = Course(
            id =id,
            name=name,
            program_id=program_id
            )
    db.session.add(new_course)
    db.session.commit()

    return jsonify({
        "message": courses +"created successfully",
        "course":{
            "id": new_course.id,
            "name": new_course.name,
            "program_id": new_course.program_id
        }}), HTTP_201_CREATED