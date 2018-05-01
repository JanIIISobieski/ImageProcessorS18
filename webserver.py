from pymodm import connect,errors
import models
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
# import decodeimage
import logging
import apifunctions as api
import IP_Functions


connect("mongodb://vcm-3483.vm.duke.edu:27017/image_app")
app = Flask(__name__)
CORS(app)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


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
    app.logger.debug('got request')
    try:
        prelim = s["originals"]  # get image files
        originals = []
        if isinstance(prelim, str):
            originals[0] = prelim
        else:
            originals = prelim
        app.logger.debug('got image')
        up_time = datetime.datetime.now()
        originals = IP_Functions.return_image_strings(originals)

        try:
            processed = []
            orig_gray = []
            size = []
            o_histogram = []
            p_histogram = []
            app.logger.debug('about to execute processing function')
            print(originals[0])
            for i, pic in enumerate(originals):
                [processed[i], orig_gray[i], size[i], o_histogram[i],
                 p_histogram[i]] = IP_Functions.run_process(pic, functions)
            app.logger.debug('executed processing function')
            ret_time = datetime.datetime.now()

            batch = []
            for i, pic in enumerate(originals):
                im = []
                im["original"] = orig_gray[i]
                im["processed"] = processed[i]
                im["original_histogram"] = o_histogram[i]
                im["processed_histogram"] = p_histogram[i]
                im["image_size"] = size[i]
                batch[i] = im
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
                api.store_uploads(email, orig_gray, up_time, functions,
                                  processed, o_histogram, p_histogram, size,
                                  ret_time)
            except errors.OperationError:
                app.logger.error('Could not store original images in database')
                return "Database is down", 503
            return jsonify(batch=batch, up_time=up_time, ret_time=ret_time,
                           functions=functions,
                           user_metrics=api.get_user_metrics(email))
        except TypeError:
            app.logger.error('Could not process uploaded images')
            return "Processing of images failed", 422
        except:
            app.logger.error('Could not process')
            return "Process failed", 422
    except TypeError:
        app.logger.error('Did not receive image encoded in base64')  # Image not
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
