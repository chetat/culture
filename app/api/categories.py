from app.api import api
from flask import jsonify, request
from models import (Users, Role,
                    Category,
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


@api.route("/categories", methods=["POST"])
def new_category():
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed!"})

    name = request.json.get("name")
    category = Category(name=name)
    try:
        Category.insert(category)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return jsonify({"error": "Could not process your request!"}), 500

    return jsonify(category.serialize), 201


@api.route('/categories', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    return jsonify({"success": True,
                    "data": [category.serialize for category in categories]})


@api.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if request.method != 'DELETE':
        return jsonify({"error": "Method not allowed!"})

    category = Category.query.filter_by(id=category_id).first()

    if not category:
        raise NotFound(f"Category with Id {category_id} not found")
    else:
        Category.delete(category)
        return jsonify(
            {
                "success": True,
                "deleted": category_id
            }), 200
