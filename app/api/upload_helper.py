from app.api import api
from flask import jsonify, request, Response
from werkzeug.utils import secure_filename
import logging
import boto3
from botocore.exceptions import ClientError
from app.config import BASE_DIR
import os
from random import randrange

from Exceptions import NotFound, MethodNotAllowed, \
    Forbiden, InternalServerError, ExistingResource,\
    BadRequest, AuthError, api_error


@api.errorhandler(BadRequest)
@api.errorhandler(Forbiden)
@api.errorhandler(MethodNotAllowed)
@api.errorhandler(InternalServerError)
def api_error(error):
    payload = dict(error.payload or ())
    payload['code'] = error.status_code
    payload['message'] = error.message
    payload['success'] = error.success
    return jsonify(payload), error.status_code


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# #Upload images to s3
@api.route("/images/upload", methods=["PUT"])
def upload_image():
    image = request.files.get("file")

    # if user does not select file, browser also
    # submit an empty part without filename
    if image is None:
        return jsonify({"error": "Provide a valid an image file"}), 400

    cover_url = ""
    upload_response = None
    if image and allowed_file(image.filename):
        # Set a random uniq string for each image
        # that will be uploaded
        filename = secure_filename(image.filename)
        image_id = f"{randrange(0, 100000)}-"
        # Name of file to be saved on AWS S3
        filename = image_id + filename

        # Store Image in local directory
        image_path = os.path.join(
            BASE_DIR + "/images_upload",
            image_id + filename)
        image.save(image_path)
        S3_BUCKET = os.environ.get("S3_BUCKET")
        upload_response = upload_file(
            image_path, S3_BUCKET, f"movies/{filename}"
        )
        # Delete file after uploaded to AWS S3 bucket
        os.remove(image_path)
    else:
        return jsonify(
            {
                "error": "Invalid extension, Jpeg, png or jpg required"
            }), 500
    if upload_response.status_code == 200:
        cover_url = f"https://{S3_BUCKET}.s3.amazonaws.com/movies/{filename}"
    else:
        raise InternalServerError("Something went wrong when saving to s3")
    return jsonify({"cover_url": cover_url})


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name,
                                         bucket,
                                         object_name)
    except ClientError as e:
        logging.error(e)
        return InternalServerError("Could Not upload file")
    return jsonify({"message": "Upload successful"})
