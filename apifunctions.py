import models
import datetime
import uuid


def existing_user_metrics(email, functions):
    """
    Update user metrics with new function calls for existing user
    :param email: username input from user (string)
    :param functions: image processing functions chosen by user (1x4 array)
    :return: save updated user metrics (1x4 array) and current timestamp
    (datetime object) in existing user object
    """
    u = models.User.objects.raw({"_id": email}).first()
    for i, n in enumerate(u.metrics):
        u.metrics[i] = u.metrics[i] + functions[i]
    u.time = datetime.datetime.now()
    u.save()


def new_user_metrics(email, functions):
    """
    Store initial user metrics for new user
    :param email: username input from user (string)
    :param functions: image processing functions chosen by user (1x4 array)
    :return: save new username (string) with initial function metrics (1x4
    array) and current timestamp (datetime object) in new user object
    """
    u = models.User(email=email, metrics=functions,
                    time=datetime.datetime.now())
    u.save()


def get_user_metrics(email):
    """
    Get user metrics for a given user
    :param email: username input from user (string)
    :return: array of function metrics for that user (1x4 array) and last
    timestamp when array was updated (datetime object)
    """
    u = models.User.objects.raw({"_id": email}).first()
    return u.metrics, u.time


def store_uploads(em, orig, up_time, funcs, proc, o_histogram,
                  p_histogram, sz, ret_time):
    """
    Store username, functions, image sizes, upload timestamp, post-processing
     timestamp, and paths to original and processed images and original and
     processed image histograms in image batch.  Assign UUID to identify image
     batch in the case that one user uploads multiple batches. Save original
     and processed images and original and processed image histograms to local
     machine using :func:`save_files`.
    :param em: username input from user (string)
    :param orig: original images encoded in base64 (array of strings)
    :param up_time: timestamp when original images were uploaded (datetime
    object)
    :param funcs: image processing functions chosen by user (1x4 array)
    :param proc: processed images encoded in base64 (array of strings)
    :param o_histogram: histograms of original images (array of strings)
    :param p_histogram: histograms of processed images (array of strings)
    :param sz: sizes of original images (array of 1x2 tuples)
    :param ret_time: post-processing timestamp (datetime object)
    :return: save all non-image inputs and paths to image files in image batch
    object, and save image files to local machine
    """
    label = uuid.uuid1()
    b = models.ImageBatch(label, em, funcs, up_time, ret_time,
                          [], [], [], [], [])
    for i, pic in enumerate(orig):
        a1 = save_files(pic)
        b.o_image.append(a1)
        a2 = save_files(proc[i])
        b.p_image.append(a2)
        a3 = save_files(o_histogram[i])
        b.o_hist.append(a3)
        a4 = save_files(p_histogram[i])
        b.p_hist.append(a4)
        tempsize = sz[i]
        b.size0.append(tempsize[0])
        b.size1.append(tempsize[1])
    b.save()
    return label


def get_latest_batch(email):
    """
    Find the most recent image batch in database for a given user and extract
    the field containing paths to processed image files.
    :param email: username input (string)
    :return: paths to processed image files (array of strings)
    """
    a = list(models.ImageBatch.objects.raw({'email': email}))
    times = []
    for i in a:
        times.append(i.ret_time)
    recent = max(times)
    b = models.ImageBatch.objects.get({'ret_time': recent})
    return b.p_image


def save_files(images):
    """
    Save encoded image to image file on local machine. Image is decoded and
    saved as JPEG file with UUID name in "imstore" directory.
    :param images: encoded image string (string)
    :return: file name of stored image (string)
    """
    import uuid
    import base64
    import os

    filename = str(uuid.uuid1())
    img = base64.b64decode(images)
    filename = filename + '.jpg'
    pathname = os.path.join('imstore/', filename)
    with open(pathname, 'wb') as file:
        file.write(img)
    return filename


def get_files(email):
    """
    Get files that are stored on local machine in "imstore" directory. Locate
    them using file names that are stored in the Image Batch object.
    :param email: username input (string)
    :return: encoded processed images (array of strings)
    """
    import base64
    import os

    im_strings = []
    batch = get_latest_batch(email)
    for pic in batch:
        pathname = os.path.join('imstore/', pic)
        with open(pathname, 'rb') as file:
            img = file.read()
        enc_img = base64.b64encode(img)
        im_strings.append(enc_img)
    return im_strings
