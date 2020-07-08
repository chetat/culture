"""from app.api import api
from flask import jsonify, request
from models import Users, Role
from app import sqlalchemy as db


@api.route("/roles", methods=["POST"])
def new_role():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")

    try:
        role = Role(name=name)
        Role.insert(role)
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(role.serialize), 201


@api.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    role = Role.query.filter_by(id=role_id).first()

    if not role:
        raise NotFound(f"Event with Id {role_id} not found")
    else:
        Role.delete(role)
        return jsonify(
            {
                "success": True,
                "deleted": role_id
            }), 200


@api.route("/roles", methods=["GET"])
def get_role():
    roles = Role.query.all()
    return jsonify([role.serialize
                    for role in roles]), 200
"""