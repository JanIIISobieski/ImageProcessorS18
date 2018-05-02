from pymodm import connect,errors
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import apifunctions as api
import IP_Functions


connect("mongodb://vcm-3483.vm.duke.edu:27017/image_app")
app = Flask(__name__)
CORS(app)


@app.route("/api/process_images", methods=["POST"])
def main_task():
    """
    Receive POST request containing an email (string), image processing
    functions (array), and base64 encoded image(s) (array).  If images are
    contained in ZIP archive, extract with
    :func:`IP_Functions.return_image_strings`.
    :func:`IP_Functions.run_process` processes images according to functions
    chosen by user, and returns metadata including histograms of original and
    processed images and image sizes.  Add base64 headers to image and
    histogram outputs.  Initialize new user or find existing user in database
    and update user metrics (number of times functions were called) along with
    current timestamp.  Log timestamps when images are uploaded and after
    images are processed.  Store original and processed images on local machine
    and store their paths and metadata in database via
    :funcs:`api.store_uploads`.
    :return: JSON containing original images, processed images, original image
    histograms, processed image histograms, image sizes, uploaded timestamp,
    post-processing timestamp; functions selected by user; user metrics
    """
    s = request.get_json()
    email = s["email"]
    functions = s["functions"]
    try:
        prelim = s["originals"]  # get image files
        originals = [0]
        if isinstance(prelim, str):
            originals[0] = prelim
        else:
            originals = prelim
        up_time = datetime.datetime.now()
        originals = IP_Functions.return_image_strings(originals)

        try:
            processed = []
            orig_gray = []
            size = []
            o_histogram = []
            p_histogram = []
            for pic in originals:
                outputs = IP_Functions.run_process(pic, functions)
                processed.append(outputs[0])
                orig_gray.append(outputs[1])
                size.append(outputs[2])
                o_histogram.append(outputs[3])
                p_histogram.append(outputs[4])
            ret_time = datetime.datetime.now()

            psend = []
            osend = []
            ohsend = []
            phsend = []
            for i, pic in enumerate(originals):
                psend.append(IP_Functions.add_header(processed[i]))
                osend.append(IP_Functions.add_header(orig_gray[i]))
                ohsend.append(IP_Functions.add_header(o_histogram[i]))
                phsend.append(IP_Functions.add_header(p_histogram[i]))

            try:
                api.existing_user_metrics(email, functions)  # update metrics
                #  for existing user
            except errors.DoesNotExist:
                api.new_user_metrics(email, functions)  # if user doesn't
                # exist, create user and set metrics
            try:
                # save images in local directory with UUID name
                api.store_uploads(email, orig_gray, up_time, functions,
                                  processed, o_histogram, p_histogram, size,
                                  ret_time)
            except errors.OperationError:
                app.logger.error('Could not store original images in database')
                return "Database is down", 503
            um = list(api.get_user_metrics(email))
            return jsonify(processed=psend, original=osend, size=size,
                           o_hist=ohsend, p_hist=phsend,
                           up_time=up_time, ret_time=ret_time,
                           functions=functions, user_metrics=um)
        except TypeError:
            app.logger.error('Type error arose when processing images')
            return "Processing of images failed, wrong type", 422
        except:
            app.logger.error('Could not process')
            return "Process failed", 422
    except TypeError:
        app.logger.error('Could not receive images or could not remove base64 '
                         'image header')  # Image not uploaded or image encoded
        #  incorrectly
        return "Images not received or in wrong format", 415


@app.route("/api/download_images", methods=["POST"])
def download_task():
    """
    Receive POST request containing username (string) and picture format
    (string). Get array of paths for processed images using
    :func:`~api.get_files`.  Use :func:`IP_Functions.resave_image` to convert
    images to correct format encoded in base64 and to put images in ZIP archive
     if there is more than one image to be returned.
    :return: base64 encoded images in correct format (JSON)
    """
    s = request.get_json()
    email = s["email"]
    im_format = s["format"]
    files = api.get_files(email)
    files = IP_Functions.resave_image(files, im_format)
    return jsonify(images=files)
