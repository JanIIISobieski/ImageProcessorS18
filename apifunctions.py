import models
import datetime


def existing_user_metrics(email, functions):
    """
    Update user metrics with new function calls for existing user
    :param email: email input from user (string)
    :param functions: image processing functions chosen by user (array)
    :return: save updated user metrics (array) and current time (datetime
    object) in existing database user object
    """
    u = models.User.objects.raw({"_id": email}).first()
    for i, n in enumerate(u.metrics):
        u.metrics[n] = u.metrics[n] + functions[n]
    u.time = datetime.datetime.now()
    u.save()


def new_user_metrics(email, functions):
    """
    Store initial user metrics for new user
    :param email: email input from user (string)
    :param functions: image processing functions chosen by user (array)
    :return: save new user (string) with initial function metrics (array) and
    current time (datetime object) in database user object
    """
    u = models.User(email=email, metrics=functions,
                    time=datetime.datetime.now())
    u.save()


def get_user_metrics(email):
    """
    Get user metrics for a given email
    :param email: email input from user (string)
    :return: array of function metrics for that user (array) and last time
    array was updated (datetime object)
    """
    u = models.User.objects.raw({"_id": email}).first()
    return [u.metrics, u.time]


# store all image batch data in database
def store_uploads(email, originals, up_time, functions, processed, o_histogram,
                  p_histogram, size, ret_time):
    """
    Store functions and paths to original images in database image batch
    :param email: email input from user (string)
    :param originals: original images encoded in base64 (array)
    :param up_time: time at which original images were uploaded (datetime
    object)
    :param functions: image processing functions chosen by user (array)
    :param processed: processed images encoded in base64 (array)
    :param o_histogram: histograms of original images (array of arrays)
    :param p_histogram: histograms of processed images (array of arrays)
    :param size: sizes of original images (array)
    :param ret_time: post-processing time (datetime object)
    :return: save array of paths to local image directories in database image
    batch object
    """
    b = models.ImageBatch(email=email)
    b.o_image = save_files(originals)
    b.up_time = up_time
    b.functions = functions
    b.p_image = save_files(processed)
    b.o_hist = o_histogram
    b.p_hist = p_histogram
    b.size = size
    b.ret_time = ret_time
    b.save()


def get_latest_batch(email):
    """
    Get the most recent image batch in database for a given user
    :param email: email input from user (string)
    :return: image batch object from database
    """
    a = models.ImageBatch.objects.get({"_id": email}).order_by('descending')
    b = a.first()
    return b


def save_files(originals):
    import uuid
    import base64
    import os

    names = []
    for pic in originals:
        filename = uuid.uuid1()
        [im_type, im_data] = pic.split(',')
        img = base64.b64decode(pic)
        if im_type == 'data:image/jpg;base64':
            filename = filename + '.jpg'
        elif im_type == 'data:image/png;base64':
            filename = filename + '.png'
        elif im_type == 'data:image/tiff;base64':
            filename = filename + '.tif'
        pathname = os.path.join('/imstore/', filename)
        with open(pathname, 'wb') as file:
            file.write(im_data)
        names.append(filename)
    return names


def get_files(email):
    import base64

    im_strings = []
    batch = get_latest_batch(email)
    for pic in batch.p_image:
        if pic.split('.')[1] == '.jpg':
            header = 'data:image/jpg;base64,'
        elif pic.split('.')[1] == '.png':
            header = 'data:image/png;base64,'
        elif pic.split('.')[1] == '.tif':
            header = 'data:image/tiff;base64,'
        with open(pic, 'rb') as file:
            img = file.read()
        enc_img = base64.b64encode(img)
        enc_img = header + enc_img
        im_strings.append(enc_img)
    return im_strings
