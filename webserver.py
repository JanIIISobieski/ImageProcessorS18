from pymodm import connect
import models
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

connect("mongodb://vcm-3483.vm.duke.edu:27017/image_app")
app = Flask(__name__)
CORS(app)

@app.route("/api/process_images",methods=["POST"])
def main_task():
    """

    :return:
    """
    try:
        # get image files
        # timestamp
        # convert files to storage format (Eitan function)
    except:
        # send frontend an error (or use status code???)
    try:
    # if user doesn't exist, create user and set metrics
    # in user array, create new subarray for user
    # subarray should contain dictionary of following keys:
        # user email
        # user metrics (function array)
        # current timestamp
    except:
    # update metrics for existing user
    # increment user metrics (function array)
    # replace timestamp with current
    try:
        # store original file directories in database (using models? see old main.py)
        # in image array, create new subarray for batch
        # subarray should contain dictionary of following keys:
            # user email
            # original images (array of directories)
            # processed images (blank for now)
            # image metadata array with dictionary:
                # up_time (current timestamp)
                # functions (function array from frontend)
    except:
        # set db flag to 1
    try:
        # for loop for each image (or will Eitan have for loop?)
            # process images (Eitan function)
            # histograms of both images (Eitan function)
            # image sizes (Eitan function)
            # timestamp
    except:
        # send frontend an error (couldn't process images)
    try:
        # store processed file directories in database
        # populate processed images key
        # populate image metadata key with dictionary:
            # original histogram
            # processed histogram
            # original image size
            # processed image size
            # ret_time (current timestamp)
    except:
        # set db flag to 1
    try:
        # jsonify all info in image array, user array, and flags
        # flags (0 error, 1 pass):