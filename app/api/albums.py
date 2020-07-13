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
Create a new Music Album
"""
@api.route("/albums", methods=["POST"])
def create_album():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    artist_id = request.json.get("artist_id")
    album_url = request.json.get("album_url")
    duration = request.json.get("duration")
    category_id = request.json.get("category_id")
    release_date = request.json.get("release_date")
    uploader_id = request.json.get("uploader_id")

    new_album = Album(
        album_name=name,
        artist_id=artist_id,
        release_date=release_date,
        category_id=category_id,
        duration=duration,
        url=album_url,
        uploader_id=uploader_id
    )

    try:
        Album.insert(new_album)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500

    return jsonify(new_album.serialize), 201


"""
Get All Albums in Database
"""
@api.route("/albums", methods=["GET"])
def get_all_albums():
    albums = Album.query.all()
    data = [album.serialize for album in albums]
    return jsonify(data), 201


"""
Delete album with given Album ID
"""
@api.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    album = Album.query.filter_by(id=album_id).first()
    if not album:
        raise NotFound(f"Event with Id {album_id} not found")
    else:
        Album.delete(album)
        return jsonify(
            {
                "success": True,
                "deleted": album_id
            }), 200


"""
Get album with given Album ID
"""
@api.route("/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    album = Album.query.filter_by(id=album_id).first()
    if not album:
        raise NotFound(f"Event with Id {album_id} not found")

    return jsonify(
            {
                "success": True,
                "data": album.serialize
            }), 200


"""
Add a user with a given role(artist, producer, composer etc..) to a track.
"""
@api.route("/tracks/<int:tack_id>/features", methods=["POST"])
def add_feature_track(track_id):
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    user_id = request.json.get("user_id")
    role_id = request.json.get("role_id")

    try:
        user_track = user_tracks.insert().values(track_id=track_id,
                                                 user_id=user_id,
                                                 role_id=role_id)
        db.session.execute(user_track)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500

    return jsonify({"success": True,
                    "message": "role_assigned"}), 200

