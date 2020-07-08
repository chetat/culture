from app.api import api
from flask import jsonify, request
from models import (Users, Role, user_type,Movie, Address, user_type)
from app import sqlalchemy as db


@api.route("/users", methods=["POST"])
def new_user():
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
    user_exist = Users.query.filter_by(email=email).first()

    if user_exist:
        return jsonify({"error": f"User with email {email} and number {phone} exist!"}), 409


    user = Users(name=name,
                 email=email,
                 aka=othername,
                 phone=phone,
                 bio=bio,)
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


@api.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    return jsonify({"success": True, "data": [user.serialize for user in users]})

@api.route('/users/movies/<int:user_id>', methods=['GET'])
def get_movies_appearance(user_id):
    user = Users.query.filter_by(id=user_id).first()
    user_mv = Movie.query.join(Users, Movie.user_id == user_id).all()

    return jsonify({"success": True,
                    "movies_appeared": [user.serialize for user in user_mv],
                    "actor": user.serialize["name"] }), 200