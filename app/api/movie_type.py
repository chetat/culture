from app.api import api
from flask import jsonify, request
from models import (Users, Role,
                    MovieType,
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


@api.route("/movies/types", methods=["POST"])
def new_type():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    movie_type = MovieType(name=name)
    try:
        MovieType.insert(movie_type)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(movie_type.serialize), 201


@api.route('/movies/types', methods=['GET'])
def get_all_types():
    movie_types = MovieType.query.all()
    return jsonify({"success": True,
                    "data": [movie_type.serialize
                             for movie_type in movie_types]})


@api.route('/movies/types/<int:type_id>', methods=['DELETE'])
def delete_movie_type(type_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    movie_type = MovieType.query.filter_by(id=type_id).first()

    if not movie_type:
        raise NotFound(f"MovieType with Id {type_id} not found")
    else:
        MovieType.delete(movie_type)
        return jsonify(
            {
                "success": True,
                "deleted": type_id
            }), 200
