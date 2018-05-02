from pymodm import fields, MongoModel


class User(MongoModel):
    """
    User model stores username in email field (string), number of times the
    user has called each function in metrics field (list of integers), and the
    most recent timestamp corresponding to an image batch upload in time
    (datetime object).
    """
    email = fields.CharField(primary_key=True)
    metrics = fields.ListField(fields.IntegerField())
    time = fields.DateTimeField()


class ImageBatch(MongoModel):
    """
    ImageBatch model stores a UUID key in identifier field (string), username
    in email field (string), functions called in functions field (list of
    integers), upload timestamp in up_time field (datetime object),
    post-processing timestamp in ret_time field (datetime object), paths to
    original images in o_image field (list of strings), paths to processed
    images in p_image field (list of strings), paths to original image
    histograms in o_hist field (list of strings), paths to processed image
    histograms in p_hist field (list of strings), first dimension of image size
    in size0 field (list of integers), and second dimension of image size in
    size1 field (list of integers).
    """
    identifier = fields.CharField(primary_key=True)
    email = fields.CharField()
    functions = fields.ListField(fields.IntegerField())
    up_time = fields.DateTimeField()
    ret_time = fields.DateTimeField()
    o_image = fields.ListField(fields.CharField())
    p_image = fields.ListField(fields.CharField())
    o_hist = fields.ListField(fields.CharField())
    p_hist = fields.ListField(fields.CharField())
    size0 = fields.ListField(fields.IntegerField())
    size1 = fields.ListField(fields.IntegerField())
