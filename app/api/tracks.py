from app.api import api
from flask import jsonify, request
from models import (Users, Role, Movie,
                    user_albums,
                    Genre,
                    Album, Track,
                    Category,
                    user_tracks,
                    user_roles)
from app import sqlalchemy as db
from Exceptions import NotFound, MethodNotAllowed, \
    Forbiden, InternalServerError, ExistingResource,\
    BadRequest, AuthError


@api.errorhandler(NotFound)
@api.errorhandler(Forbiden)
@api.errorhandler(MethodNotAllowed)
@api.errorhandler(InternalServerError)
def api_error(error):
    payload = dict(error.payload or ())
    payload['code'] = error.status_code
    payload['message'] = error.message
    payload['success'] = error.success
    return jsonify(payload), error.status_code


"""
Create a new Track
"""
@api.route("/tracks", methods=["POST"])
def create_track():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    title = request.json.get("title")
    artist_id = request.json.get("artist_id")
    track_url = request.json.get("track_url")
    genre_id = request.json.get("genre_id")
    category_id = request.json.get("category_id")
    duration = request.json.get("duration")
    release_date = request.json.get("release_date")
    uploader_id = request.json.get("uploader_id")
    album_id = request.json.get("album_id")

    new_track = Track(
        song_title=title,
        genre_id=genre_id,
        url=track_url,
        category_id=category_id,
        artist_id=artist_id,
        release_date=release_date,
        duration=duration,
        album_id=album_id,
        uploader_id=uploader_id
    )

    try:
        Track.insert(new_track)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500
    return jsonify(new_track.serialize), 201

"""
Get All tracks in Database
"""
@api.route("/tracks", methods=["GET"])
def get_all_tracks():
    tracks = Track.query.all()

    data = []
    for track in tracks:
        artist = Users.query.filter_by(id=track.artist_id).first()
        album = Album.query.filter_by(id=track.album_id).first()

        temp = {
            "id": track.id,
            "track_link": track.url,
            "song_title": track.song_title,
            "duration": track.duration,
            "release_date": track.release_date,
            "artist": artist.aka,
            "album": album.album_name
        }
        data.append(temp)

    return jsonify(data), 200
