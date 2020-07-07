from app.api import api
from flask import jsonify, request
from models import (Users, Profession, user_roles, user_profession)
from app import sqlalchemy as db


@api.route("/movies", methods=["POST"])
def new_movie():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    email = request.json.get("email")
    othername = request.json.get("othername")
    phone = request.json.get("phone")
    city = request.json.get("city")
    prof_ids = request.json.get("profession_id")
    role_id = request.json.get("role_id")
    user_exist = Users.query.filter_by(email=email).first()

    if user_exist:
        return jsonify({"error": f"User with email {email} and number {phone} exist!"}), 409
    user = Users(name=name,
                 email=email,
                 aka=othername,
                 phone=phone,
                 city=city
                 )
    try:
        # Create user, get user id and create profession using 
        # profession_id and user id created
        Users.insert(user)
        for item in prof_ids:
            user_prof = user_profession.insert().values(profession_id=item,
                                                    user_id=user.id)
            db.session.execute(user_prof)

        user_role = user_roles.insert().values(role_id=role_id,
                                                    user_id=user.id)
        db.session.execute(user_role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(user.serialize), 201


@api.route('/movies', methods=['GET'])
def get_all_movies():
    users = Users.query.all()
    return jsonify({"success": True, "data": [user.serialize for user in users]})