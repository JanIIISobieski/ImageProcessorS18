from pymodm import fields, MongoModel


class User(MongoModel):
    email = fields.CharField(primary_key=True)
    metrics = fields.ListField(fields.IntegerField())
    time = fields.DateTimeField()


class ImageBatch(MongoModel):
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

