from app.api import api
from flask import jsonify, request
from models import Users, UType
from app import sqlalchemy as db


@api.route("/user-types", methods=["POST"])
def new_utype():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")

    try:
        utype = UType(name=name)
        UType.insert(utype)
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(utype.serialize), 201


@api.route("/user-types", methods=["GET"])
def get_u_type():
    user_types = UType.query.all()
    return jsonify([u_type.serialize for u_type in user_types]), 200


@api.route("/user-types/<int:type_id>", methods=["DELETE"])
def delete_type(type_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    utype = UType.query.filter_by(id=role_id).first()
    if not utype:
        raise NotFound(f"Event with Id {type_id} not found")
    else:
        UType.delete(utype)
        return jsonify(
            {
                "success": True,
                "deleted": type_id
            }), 200
