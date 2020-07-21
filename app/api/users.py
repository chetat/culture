from app.api import api
from flask import jsonify, request
from models import (Users, Role, user_type, Album, Genre,
                    movies_appear, user_albums, Category,
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
    photo = request.json.get("photo")

    user_exist = Users.query.filter_by(email=email).first()

    if user_exist:
        return jsonify({
            "error": f"User with email {email} and number {phone} exist!"
        }), 409

    user = Users(
        name=name,
        email=email,
        aka=othername,
        phone=phone,
        bio=bio,
        profile_pic=photo
    )

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


"""
Update user
"""
@api.route("/users/<int:id>", methods=["PATCH"])
def update_user(id):
    if request.method != 'PATCH':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    email = request.json.get("email")
    othername = request.json.get("othername")
    phone = request.json.get("phone")
    city = request.json.get("city")
    utype_id = request.json.get("utype_id")
    region = request.json.get("region")
    bio = request.json.get("bio")
    photo = request.json.get("photo")

    user = Users.query.filter_by(id=id).first()

    if user:
        user.name = name
        user.email = email
        user.aka = othername
        user.phone = phone
        user.bio = bio
        user.profile_pic = photo

        Users.update(user)

    return jsonify(user.serialize), 201


"""
Get all movies where user participated or featured
in anyway
"""
@api.route('/users/<int:user_id>/details', methods=['GET'])
def get_user_appearance(user_id):
    user = Users.query.filter_by(id=user_id).first()
    movies_appearance = db.session.query(movies_appear).filter(
        movies_appear.c.user_id == user_id).all()

    album_appearance = db.session.query(user_albums).filter(
        user_albums.c.user_id == user_id).all()

    movies_data = []
    for mov_ap in movies_appearance:
        role = Role.query.filter_by(id=mov_ap.role_id).first()
        movie = Movie.query.filter_by(id=mov_ap.movie_id).first()
        genre = Genre.query.filter_by(id=movie.serialize["genre_id"]).first()
        cat = Category.query.filter_by(
            id=movie.serialize["category_id"]).first()
        if movie:
            temp = {
                "id": movie.id,
                "title": movie.title,
                "category": cat.serialize["name"],
                "roles": role.name,
                "cover_url": movie.cover_url
            }
            movies_data.append(temp)

    movies_feat_data = {}
    for mov in movies_data:
        keys, values = list(mov.keys()), list(mov.values())
        # Check if role(index 2) exists in each users_featured dict
        # and assign a new dictionary value with id, role name, and user name as keys
        # if key(role) exists, assign it the role value(ex: sound Engineer).
        if keys[3] in movies_feat_data:
            movies_feat_data[keys[0]] = values[0]
            movies_feat_data[keys[1]] = values[1]
            movies_feat_data[keys[2]] = values[2]
            movies_feat_data[keys[3]].append(values[3])
            movies_feat_data[keys[4]] = values[4]
        else:
            movies_feat_data[keys[0]] = values[0]
            movies_feat_data[keys[1]] = values[1]
            movies_feat_data[keys[2]] = values[2]
            movies_feat_data[keys[3]] = [values[3]]
            movies_feat_data[keys[4]] = values[4]

    album_data = []
    for album_ap in album_appearance:
        role = Role.query.filter_by(id=album_ap.role_id).first()
        album = Album.query.filter_by(id=album_ap.album_id).first()
        cat = Category.query.filter_by(
            id=album.serialize["category_id"]).first()
        temp = {
            "id": album.id,
            "album_name": album.album_name,
            "cover_url": album.album_cover_url,
            "roles": role.name,
            "category": cat.name
        }
        album_data.append(temp)

    album_feat_data = {}
    for alb in album_data:
        keys, values = list(alb.keys()), list(alb.values())
        # Check if role(index 2) exists in each users_featured dict
        # and assign a new dictionary value with id, role name, and user name as keys
        # if key(role) exists, assign it the role value(ex: sound Engineer).
        if keys[3] in album_feat_data:
            album_feat_data[keys[0]] = values[0]
            album_feat_data[keys[1]] = values[1]
            album_feat_data[keys[2]] = values[2]
            album_feat_data[keys[3]].append(values[3])
            album_feat_data[keys[4]] = values[4]
        else:
            album_feat_data[keys[0]] = values[0]
            album_feat_data[keys[1]] = values[1]
            album_feat_data[keys[2]] = values[2]
            album_feat_data[keys[3]] = [values[3]]
            album_feat_data[keys[4]] = values[4]

    return jsonify({"success": True,
                    "albums_appeared": [album_feat_data] if album_feat_data else [],
                    "movies_appeared": [movies_feat_data] if movies_feat_data else [],
                    "user": {
                        "id": user.serialize["id"],
                        "name": user.serialize["name"],
                        "aka": user.serialize["other_name"],
                        "bio": user.serialize["bio"],
                        "image": user.serialize["image"]
                    }}), 200
