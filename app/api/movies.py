from app.api import api
from flask import jsonify, request
from models import (Users, Role, Movie, movies_appear, Genre, Category,
                    user_roles)
from app import sqlalchemy as db

"""
Create a new Movie
"""
@api.route("/movies", methods=["POST"])
def create_movie():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    title = request.json.get("title")
    synopsis = request.json.get("synopsis")
    pg = request.json.get("pg")
    trailer_url = request.json.get("trailer_url")
    duration = request.json.get("duration")
    release_date = request.json.get("release_date")
    genre_id = request.json.get("genre_id")
    uploader_id = request.json.get("uploader_id")
    category_id = request.json.get("category_id")

    exist_movie = Movie.query.filter_by(title=title).first()

    # Check if movie with the same title exists and return error if true
    if exist_movie:
        return jsonify({
            "error": f"Movie with title {exist_movie} Exists!"}), 409

    new_movie = Movie(
        title=title,
        synopsis=synopsis,
        parental_guide=pg,
        release_date=release_date,
        duration=duration,
        trailer_url=trailer_url,
        uploader_id=uploader_id,
        genre_id=genre_id,
        category_id=category_id
    )

    try:
        Movie.insert(new_movie)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500

    return jsonify(new_movie.serialize), 201

"""
Get all movies
"""
@api.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    movies_data = [movie.serialize for movie in movies]

    return jsonify({"success": True,
                    "data": movies_data}), 200


"""
Get Movie details with movie ID given
"""
@api.route('/movies/<int:movie_id>', methods=['GET'])
def get_single_movie(movie_id):
    data = db.session.query(movies_appear).all()
    user_data = []
    movie = Movie.query.filter_by(id=movie_id).first()
    movies_appearance = db.session.query(movies_appear).filter(
        movies_appear.c.movie_id == movie_id).all()

    for mov_ap in movies_appearance:
        user = Users.query.filter_by(id=mov_ap.user_id).first()
        user_data.append(user.serialize)

    return jsonify({"success": True,
                    "actors": user_data,
                    "movie": movie.serialize
                    }), 200


"""
Attach a user and user role to a movie
"""
@api.route("/movies/<int:movie_id>/members", methods=["POST"])
def add_appearance_movie(movie_id):
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    user_id = request.json.get("member_id")
    role_id = request.json.get("role_id")

    try:
        user_movie = movies_appear.insert().values(movie_id=movie_id,
                                                   user_id=user_id,
                                                   role_id=role_id)
        db.session.execute(user_movie)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500

    return jsonify({"success": True,
                    "message": "role_assigned"}), 200

"""
Get all movies where user participated or featured
in anyway
"""
@api.route('/movies/users/<int:user_id>/appearance', methods=['GET'])
def get_user_appearance(user_id):
    user = Users.query.filter_by(id=user_id).first()
    movies_appearance = db.session.query(movies_appear).filter(
        movies_appear.c.user_id == user_id).all()

    movies_data = []
    for mov_ap in movies_appearance:
        role = Role.query.filter_by(id=mov_ap.role_id).first()
        print(role.name)
        movie = Movie.query.filter_by(id=mov_ap.movie_id).first()
        genre = Genre.query.filter_by(id=movie.serialize["genre_id"]).first()
        cat = Category.query.filter_by(id=movie.serialize["category_id"]).first()

        movies_data.append({
                "id": movie.serialize["id"],
                "title": movie.serialize["title"],
                "synopsis": movie.serialize["synopsis"],
                "pg": movie.serialize["pg"],
                "genre": genre.serialize["name"],
                "category": cat.serialize["name"],
                "release_date": movie.serialize["release_date"],
                "duration": movie.serialize["duration"],
                "trailer_url": movie.serialize["trailer_url"]
            })

    return jsonify({"success": True,
                    "movies_appeared": movies_data,
                    "actor": {
                        "id": user.serialize["id"],
                        "name": user.serialize["name"],
                        "aka": user.serialize["other_name"],
                        "bio": user.serialize["bio"]
                        }}), 200
