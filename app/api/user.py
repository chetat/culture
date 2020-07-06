from app.api import api
from flask import jsonify, request
from models import Users
from app import sqlalchemy as db


@api.route("/")
def users():
    return "hello"


@api.route("/users", methods=["POST"])
def new_user():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    email = request.json.get("email")
    phone = request.json.get("phone")

    user_exist = Users.query.filter_by(email=email).first()

    if user_exist:
        return jsonify({"error": f"User with email {email} and number {phone} exist!"}), 409

    user = Users(first_name=firstname, last_name=lastname,
                 email=email, phone=phone)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(user.serialize), 201


@api.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = Users.query.all()
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error! Could not retrieve users."})

    return jsonify({"success": True, "data": [user.serialize for user in users]})
