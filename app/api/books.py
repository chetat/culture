from app.api import api
from flask import jsonify, request
from models import (Users, Role,
                    Genre, Book,
                    Category,
                    user_books,
                    user_roles)
from app import sqlalchemy as db

"""
Create a new Book
"""
@api.route("/books", methods=["POST"])
def create_book():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("title")
    author_id = request.json.get("author_id")
    category_id = request.json.get("category_id")
    genre_id = request.json.get("genre_id")
    book_url = request.json.get("book_url")
    release_date = request.json.get("release_date")
    uploader_id = request.json.get("uploader_id")

    new_book = Book(
        book_name=name,
        author_id=author_id,
        release_date=release_date,
        genre_id=genre_id,
        url=book_url,
        category_id=category_id,
        uploader_id=uploader_id
    )

    try:
        Book.insert(new_book)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500
    return jsonify(new_book.serialize), 201


"""
Add a user with a given role(publisher, producer, composer etc..) to a track.
"""
@api.route("/books/<int:book_id>/features", methods=["POST"])
def add_feature_book(track_id):
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    user_id = request.json.get("user_id")
    role_id = request.json.get("role_id")

    try:
        user_book = user_books.insert().values(book_id=book_id,
                                               user_id=user_id,
                                               role_id=role_id)
        db.session.execute(user_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({
            "error": "Could not process your request!"}), 500

    return jsonify({"success": True,
                    "message": "role_assigned"}), 200
