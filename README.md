Django Autofields
=============================

This app contains a couple of fields which do some amount of processing data 
munging, or prepopulate from other fields.

`AutoSlugField`
-----------------------------

The `AutoSlugField` is a slug field which can be auto-populated at creation-time 
from the contents of another field. It supports enforcing uniqueness, both over
the entire model, and depending on the contents of certain fields (the 
`field__value` syntax is supported).

Example:

    class MyNonUniqueModel(models.Model):
        name = models.CharField(max_length=255)
        slug = AutoSlugField(prepopulate_from='name')

    class MyNormalUniqueModel(models.Model):
        name = models.CharField(max_length=255)
        slug = AutoSlugField(prepopulate_from='name', unique=True)

    class MyModel(models.Model):
        name = models.CharField(max_length=255)
        date = models.DateField()
        slug = AutoSlugField(
                    prepopulate_from='name', 
                    unique_for_fields=['date__year', 'date__month']
               )

In the first example, the slug will simply by the slugified value of the
name field.

In the second example, the slug will be unique over the the entire model.

In the last example, the slug will be unique for the year and month of 
the `date` field on the instance.

The slug will only ever be generated at creation time (to avoid having a URL 
change just from a changed title), and only if the slug was not set explicitly
prior to save.

When uniquifying the slug, the `settings.AUTOSLUG_FORMAT` setting is used, which
by default is `'%s_%s`. This will generate slugs in the form `slug-1`, `slug-2',
etc. when a unique

AutoMarkdownTextField
-----------------------------

The `AutoMarkdownTextField` is a text field which is auto-populated at save-time 
from the contents of another field, and then has the markdown filter run over it.

Example:

    class MyModel(models.Model):
        content_raw = models.TextField()
        content = AutoMarkdownTextField(prepopulate_from='content_raw')

When generating the markdown to store in the DB, the `settings.AUTOMARKDOWN_EXTENSIONS`
setting is used, which is a list of markdown extension names to use. By default
the list is empty, but it can be set to something like `['codehilite',]` if you
have Pygments installed to force syntax highlighting, etc.

SerializedDataField
-----------------------------

The `SerializedDataField` is a field which stores pickled python objects and 
allows access to them as normal python objects directly.

On Running Tests
-----------------------------

Make sure to add autofields.test to `INSTALLED_APPS` in order to run
unit tests, as the tests include their own models which need to be
discovered on test runs.
