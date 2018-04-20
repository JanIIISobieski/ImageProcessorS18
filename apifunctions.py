import models
import datetime


# update existing user's metrics
def existing_user_metrics(email, functions):
    u = models.User.objects.raw({"_id": email}).first()
    for i, n in enumerate(u.metrics):
        u.metrics[n] = u.metrics[n] + functions[n]
    u.time = datetime.datetime.now()
    u.save()


# create new user
def new_user_metrics(email, functions):
    u = models.User(email, functions, datetime.datetime.now())


# store originals, functions, up_time in db
def store_uploads(email, originals, up_time, functions):
    b = models.ImageBatch(email)
    b.o_image = originals
    b.up_time = up_time
    b.functions = functions
    b.save()


# store processed, histograms, sizes, rettime in db
def store_returns(email, processed, o_histogram, p_histogram, o_size, p_size):
    a = models.ImageBatch.objects.get({"_id": email}).order_by('descending')
    b = a.first()
    b.p_image = processed
    b.o_hist = o_histogram
    b.p_hist = p_histogram
    b.o_size = o_size
    b.p_size = p_size
    b.ret_time = datetime.datetime.now()
    b.save()
