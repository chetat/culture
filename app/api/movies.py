from app.api import api
from flask import jsonify, request
from models import (Users, Role, Movie, movies_appear,
                    user_roles)
from app import sqlalchemy as db


"""
date_time_str = '28 June 2018'
date_object = datetime.strptime(date_string, "%d %B, %Y")
date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y')
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
    user_id = request.json.get("user_id")
    category_id = request.json.get("category_id")

    exist_movie = Movie.query.filter_by(title=title).first()

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
        user_id=user_id,
        genre_id=genre_id,
        category_id=category_id
    )

    try:
        Movie.insert(new_movie)
        user_movie = movies_appear.insert().values(movie_id=new_movie.id,
                                                   user_id=user_id)
        db.session.execute(user_movie)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500

    return jsonify(new_movie.serialize), 201


@api.route('/movies', methods=['GET'])
def get_all_movies():
    """# Get movies where user features
    Artist.query.join(Artist.albums).filter_by(genre_id=genre.id).all()
    user_mv = Movie.query.join(Users, Users.id == Movie.user_id).all()
    print(user_mv)"""
    movies = Movie.query.all()
    movies_data = [movie.serialize for movie in movies]

    return jsonify({"success": True,
                    "data": movies_data}), 200


@api.route('/movies/cast/<int:movie_id>', methods=['GET'])
def get_single_movies(movie_id):
    # movie_casts = Movie.query.filter(Movie.mov_appear.any(movie_id=movie_id)).all()
    # venues_all = Venue.query.join(Artist, Venue.state == Artist.state).all()
    # data = db.session.query(movies_appear).all()

    data = db.session.query(movies_appear).all()
    user_data = []
    movie = Movie.query.filter_by(id=movie_id).first()
    movies_appearance = db.session.query(movies_appear).filter(movies_appear.c.movie_id == movie_id).all()   

    for mov_ap in movies_appearance:
        user = Users.query.filter_by(id=mov_ap.user_id).first()
        user_data.append(user.serialize)
    return jsonify({"success": True,
                    "actors": user_data,
                    "movie": movie.serialize["title"]
                    }), 200
