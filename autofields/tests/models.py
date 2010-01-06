from django.db import models
from .. import fields

class TestAutoDescriptionModel(models.Model):
    text = models.TextField()
    html = fields.AutoMarkdownTextField(prepopulate_from = "text")
    nonpop = fields.AutoMarkdownTextField()
    nonupdate = fields.AutoMarkdownTextField(prepopulate_from = "text", only_on_create = True)

class TestAutoSlugModel(models.Model):
    name = models.CharField(max_length = 255)
    slug = fields.AutoSlugField(prepopulate_from = "name", unique = False)
    uniq = fields.AutoSlugField(prepopulate_from = "name", unique = True)
    nonpop = fields.AutoSlugField()

class TestFieldUniqueSlugModel(models.Model):
    name = models.CharField(max_length = 255)
    date = models.DateField()
    slug = fields.AutoSlugField(prepopulate_from = "name", unique = True)
    uniq = fields.AutoSlugField(prepopulate_from = "name", unique_for_fields = ["date__year", "date__month", "date__day"])

class TestSerializedDataModel(models.Model):
    data = fields.SerializedDataField(null = True)
