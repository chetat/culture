from app.api import api
from flask import jsonify, request
from models import Users, Role, Profession
from app import sqlalchemy as db


@api.route("/professions", methods=["POST"])
def new_profession():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")

    try:
        profession = Profession(name=name)
        Profession.insert(profession)
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(profession.serialize), 201


@api.route("/professions/<int:prof_id>", methods=["DELETE"])
def delete_profession(prof_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    profession = Profession.query.filter_by(id=prof_id).first()

    if not profession:
        raise NotFound(f"Event with Id {event_id} not found")
    else:
        Profession.delete(profession)
        return jsonify(
            {
                "success": True,
                "deleted": prof_id
            }), 200


@api.route("/professions", methods=["GET"])
def get_profession():
    professions = Profession.query.all()
    return jsonify([profession.serialize
                    for profession in professions]), 200
