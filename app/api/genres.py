from app.api import api
from flask import jsonify, request
from models import (Users, Role,
                    Genre,
                    user_roles)
from app import sqlalchemy as db


@api.route("/categories/<int:category_id>/genres", methods=["POST"])
def new_genre(category_id):
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    genre = Genre(name=name, category_id=category_id)

    try:
        Genre.insert(genre)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(genre.serialize), 201


@api.route('/categories/<int:cat_id>/genres', methods=['GET'])
def get_all_genres(cat_id):
    genres = Genre.query.filter_by(category_id=cat_id)
    return jsonify({"success": True,
                    "data": [genre.serialize for genre in genres]})


@api.route('/categories/genres/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    genre = Genre.query.filter_by(id=genre_id).first()

    if not genre:
        raise NotFound(f"Event with Id {genre_id} not found")
    else:
        Genre.delete(genre)
        return jsonify(
            {
                "success": True,
                "deleted": genre_id
            }), 200
