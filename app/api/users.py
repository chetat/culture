from app.api import api
from flask import jsonify, request
from models import (Users, Role, user_type,
                     Movie, Address, user_type)
from flask_bcrypt import check_password_hash
from app import sqlalchemy as db


"""
Add a new user
"""
@api.route("/users", methods=["POST"])
def register_user():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    email = request.json.get("email")
    othername = request.json.get("othername")
    phone = request.json.get("phone")
    city = request.json.get("city")
    utype_id = request.json.get("utype_id")
    region = request.json.get("region")
    bio = request.json.get("bio")
    password = request.json.get("password")

    user_exist = Users.query.filter_by(email=email).first()

    if user_exist:
        return jsonify({
            "error": f"User with email {email} and number {phone} exist!"
        }), 409

    user = Users(name=name,
                 email=email,
                 aka=othername,
                 phone=phone,
                 bio=bio)

    user.set_password(password)

    try:
        # Create user, get user id and create role
        # using
        # role_id and user id created
        Users.insert(user)
        address = Address(
                    city=city,
                    region=region,
                    user_id=user.id)
        Address.insert(address)
        user_typ = user_type.insert().values(utype_id=utype_id,
                                             user_id=user.id)
        db.session.execute(user_typ)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(user.serialize), 201

"""
Get all users in all the database
"""
@api.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    return jsonify({"success": True,
                   "data": [user.serialize for user in users]})


@api.route('/auth/login', methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = Users.query.filter_by(email=email).first()

    if not user:
        raise NotFound(f"User with email {email} does not exist")
    else:
        return True
