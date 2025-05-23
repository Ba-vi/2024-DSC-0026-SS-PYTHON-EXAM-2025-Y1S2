from app.extensions import db
from app.models.program_model import Program
from flask import Blueprint, jsonify, request
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR


programs = Blueprint("programs", __name__, url_prefix='/api/v1/programs')

# creating a program
@programs.route('/register', methods=['POST'])
def register_program():
    data = request.get_json()
    program_id =data.get("program_id")
    name = data.get("name")
    description = data.get("description")

    if not program_id or  not name or not description:
        return jsonify({"Error":"All fields are required."}),HTTP_400_BAD_REQUEST
    try:
            new_program = Program(
                program_id=program_id,
                name=name, 
                description=description
                )
            db.session.add(new_program)
            db.session.commit()

            return jsonify({
                "message": "Program created successfully", 
                "program":{
                    "id": new_program.program_id,
                    "name": new_program.name,
                    "description": new_program.description,
                    "created_at": new_program.created_at,
                    "updated_at": new_program.updated_at
                }
                }), HTTP_201_CREATED
    except Exception as e:  
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the program"}), HTTP_500_INTERNAL_SERVER_ERROR

#updating a program by proram_id
@programs.route('/update/<int:program_id>', methods=['PUT'])
def update_program(program_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

  
    program = Program.query.get(program_id)#querying the program by id

    #validating the program
    if not program:
        return jsonify({"Error": "Program not found"}), HTTP_404_NOT_FOUND
    # checking if the name is provided
    
    if name:
        program.name = name
    # checking if the description is provided
    if description:
        program.description = description

    db.session.commit()

    return jsonify({
        "message": "Program updated successfully", 
        "program":{
            "id": program.program_id,
            "name": program.name,
            "description": program.description,
            "created_at": program.created_at,
            "updated_at": program.updated_at
        }
          }), HTTP_200_OK