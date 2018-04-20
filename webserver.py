from pymodm import connect
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

@app.route("/api/process_images",methods=["POST"])
def main_task():
    """

    :return:
    """
    s = request.get_json()
    email = s["email"]
    functions = s["functions"]
    up_time = datetime.datetime.now()
    try:
        originals = s["originals"] # get image files
        # verify that images are encoded in base64
        try:
            api.existing_user_metrics(email, functions) # update metrics for existing user
        except:
            api.new_user_metrics(email, functions) # if user doesn't exist, create user and set metrics
        try:
            # save images in local directory with UUID name
            api.store_uploads(email, originals, up_time, functions)  # store original file directories in database
        except:
            logging.error('Could not save images to database')
        try:
            # for loop for each image (or will Eitan have for loop?)
                # process images (Eitan function)
                # histograms of both images (Eitan function)
                # image sizes (Eitan function)
                # timestamp
            try:
                api.store_returns(email, processed, o_histogram, p_histogram, o_size, p_size) # store processed images and data in database
            except:
                logging.error('Could not store processed images in database')
        except:
            logging.error('Could not process uploaded images')
        # jsonify all info in image array, user array, and flags
    except:
        logging.error('Did not receive image encoded in base64') # Image not uploaded or encoded incorrectly
