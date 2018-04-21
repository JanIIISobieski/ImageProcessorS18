from pymodm import connect,errors
import models
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import decodeimage
import logging
import apifunctions as api
import datetime


connect("mongodb://vcm-3483.vm.duke.edu:27017/image_app")
app = Flask(__name__)
CORS(app)


@app.route("/api/process_images", methods=["POST"])
def main_task():
    """
    Receive POST request containing an email (string), image processing
    functions (array), and base64 encoded image(s) (array).  Initialize new
    user or find existing user in database and update user metrics (number of
    times functions were called) along with current time.  Process images
    according to functions chosen by user, and return metadata including
    histograms of original and processed images and sizes of original and
    processed images.  Log time when images are uploaded and after images are
    processed.  Store original and processed images on local machine and
    store their paths in database, along with associated metadata.
    :return: Original images, histograms, and sizes; processed images,
    histograms, and sizes; uploaded time; post-processing time; functions
    selected by user; user metrics (JSON)
    """
    s = request.get_json()
    email = s["email"]
    functions = s["functions"]
    try:
        originals = s["originals"]  # get image files
        up_time = datetime.datetime.now()
        # verify that images are encoded in base64

        try:
            for i,n in enumerate(originals):
                processed = process_image(i, functions)
                o_histogram = histogram(i)
                p_histogram = histogram(processed)
                o_size = get_size(i)
                p_size = get_size(processed)
            ret_time = datetime.datetime.now()

            batch = []
            for i, n in enumerate(originals):
                im = []
                im["original"] = i
                im["processed"] = processed[n]
                im["original_histogram"] = o_histogram[n]
                im["processed_histogram"] = p_histogram[n]
                im["original_size"] = o_size[n]
                im["processed_size"] = p_size[n]
                batch[n] = im
            try:
                api.existing_user_metrics(email,
                                          functions)  # update metrics for
                #  existing user
            except errors.DoesNotExist:
                api.new_user_metrics(email,
                                     functions)  # if user doesn't exist,
                # create user and set metrics
            try:
                # save images in local directory with UUID name
                api.store_uploads(email, originals, up_time,
                                  functions)
            except errors.OperationError:
                logging.error('Could not store original images in database')
                return "Database is down", 503
            try:
                api.store_returns(email, processed, o_histogram, p_histogram,
                                  o_size, p_size, ret_time)  # store processed
                # images and data in database
            except errors.OperationError:
                logging.error('Could not store processed images in database')
                return "Database is down", 503
            return jsonify(batch=batch, up_time=up_time, ret_time=ret_time,
                           functions=functions,
                           user_metrics=api.get_user_metrics(email))
        except TypeError:
            logging.error('Could not process uploaded images')
            return "Processing of images failed", 422
    except TypeError:
        logging.error('Did not receive image encoded in base64')  # Image not
        # uploaded or image encoded incorrectly
        return "Images in wrong format", 415


@app.route("/api/download_images", methods=["GET"])
def download_task():
    """
    Receive GET request containing email (string) and picture format (string).
    Get latest image batch for user and convert images to correct format
    encoded in base64
    :return: base64 encoded images in correct format (JSON)
    """
    s = request.get_json()
    email = s["email"]
    im_format = s["format"]
    files = api.get_latest_batch(email)
