import models
import datetime
import uuid


def existing_user_metrics(email, functions):
    """
    Update user metrics with new function calls for existing user
    :param email: username input from user (string)
    :param functions: image processing functions chosen by user (array)
    :return: save updated user metrics (array) and current time (datetime
    object) in existing database user object
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
    :param email: username input from user (string)
    :return: array of function metrics for that user (array) and last time
    array was updated (datetime object)
    """
    u = models.User.objects.raw({"_id": email}).first()
    return u.metrics, u.time


# store all image batch data in database
def store_uploads(em, orig, up_time, funcs, proc, o_histogram,
                  p_histogram, sz, ret_time):
    """
    Store functions and paths to original images in database image batch
    :param email: username input from user (string)
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
    Get the most recent image batch in database for a given user
    :param email: username input (string)
    :return: image batch object from database
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
    Save encoded images to image files on local machine. Images will be saved
    as JPEG files with UUID names in "imstore" directory.
    :param images: array of encoded images
    :return: array of file names for stored images
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
    :return: array of encoded images (post-processing)
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
