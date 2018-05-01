from pymodm import fields, MongoModel


class User(MongoModel):
    email = fields.CharField(primary_key=True)
    metrics = fields.ListField(fields.IntegerField())
    time = fields.DateTimeField()


class ImageBatch(MongoModel):
    email = fields.CharField(primary_key=True)
    o_image = fields.ListField(fields.CharField())
    p_image = fields.ListField(fields.CharField())
    up_time = fields.DateTimeField()
    functions = fields.ListField(fields.IntegerField())
    o_hist = fields.ListField(fields.CharField())
    p_hist = fields.ListField(fields.CharField())
    size0 = fields.ListField(fields.IntegerField())
    size1 = fields.ListField(fields.IntegerField())
    ret_time = fields.DateTimeField()
