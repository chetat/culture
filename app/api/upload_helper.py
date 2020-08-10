from app.api import api
from flask import jsonify, request


# #Upload images to s3
@api.route("/images/upload", methods=["PUT"])
def upload_imageg():
    print(request.headers)
    image = request.files
    return jsonify({"hi": "How you"})
