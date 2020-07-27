from app.api import api
from flask import jsonify, request
from models import (Users, Role, Movie, movies_appear, Genre, Category,
                    user_roles)
from app import sqlalchemy as db
from itertools import groupby


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
    cover_url = request.json.get("cover_url")

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
        category_id=category_id,
        cover_url=cover_url
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

# This function returns movie release year


def grouper(movie):
    return movie.release_date.year


@api.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.order_by(Movie.release_date).all()

    # Group movies release in same year with groupby iterator
    """group_data = [(year, list(it.serialize for it in items))
                  for year, items in groupby(movies, grouper)]"""
    serialized_data = [movie.serialize for movie in movies]
    # Iterates through iter objects return by group data
    # and covert to dict
    #serialized_data = dict([(year, data) for year, data in group_data])
    return jsonify({"success": True,
                    "data": serialized_data}), 200


"""
Get Movie details with movie ID given
"""
@api.route('/movies/<int:movie_id>', methods=['GET'])
def get_single_movie(movie_id):
    # data = db.session.query(movies_appear).all()
    user_data = []
    movie = Movie.query.filter_by(id=movie_id).first()
    movies_appearance = db.session.query(movies_appear).filter(
        movies_appear.c.movie_id == movie_id).all()

    cat = Category.query.filter_by(id=movie.category_id).first()
    genre = Genre.query.filter_by(id=movie.serialize["genre_id"]).first()

    for mov_ap in movies_appearance:
        user = Users.query.filter_by(id=mov_ap.user_id).first()
        user_data.append({
            "id": user.id,
            "name": user.name
        })
    data = {
        "id": movie.id,
        "title": movie.title,
        "synopsis": movie.synopsis,
        "pg": movie.parental_guide,
        "genre": genre.name,
        "category": cat.name,
        "release_date": movie.release_date.strftime("%d-%m-%Y"),
        "duration": movie.duration,
        "trailer_url": movie.trailer_url,
        "cover_url": movie.cover_url
    }
    return jsonify({"success": True,
                    "actors": user_data,
                    "movie": data
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
Delete album with given Album ID
"""
@api.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        raise NotFound(f"Event with Id {movie_id} not found")
    else:
        Movie.delete(movie)
        return jsonify(
            {
                "success": True,
                "deleted": movie_id
            }), 200
