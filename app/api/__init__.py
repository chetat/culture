from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1')

from . import (
    users, roles, roles, movies, categories,
    genres, u_type, albums, books, tracks, movie_type,
    upload_helper
    )
