from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.conf import settings

from . import setting

def countup(start=1):
    while True:
        yield start
        start = start + 1

class AutoSlugField(SlugField):
    """
    A slug field which can be automatically generated, assuming no slug
    has been given to the model prior to saving. If you assign a slug during
    or after creation, that is the slug that will be used.

    Slug options are as follows:
        - C{prepopulate_from}: If this field is given, the slug will be prepopulated
          from the value of the field with the given name. Note that without this
          option set, this field acts as a normal SlugField
        - C{unique_for_fields}: This field acts like C{unique}, with two major differences:
            1. The uniqueness is only guaranteed through the model class, not the database,
               meaning you can insert duplicate values directly into the DB, or through some
               sort of threading race condition.
            2. The uniqueness only applies to objects that are unique in the given fields. This
               is best explained by example::

                    class SomeModel(models.Model):
                        name = models.CharField(max_length=255)
                        date = models.DateTimeField()
                        slug = AutoSlugField(
                                    prepopulate_from='name',
                                    unique_for_fields=['date__year', 'date__month']
                               )

               In that model, the slug field will be required to be unique for the year and
               month parts of the date field. So, an instance with C{name="FooBar"} and C{date=date(2009, 8, 1)}
               could have the same slug as one with the same name, but a date of C{date=date(2009, 7, 1)}.

    Additionally, AutoSlugField responds to the C{settings.AUTOSLUG_FORMAT} setting, using it
    to format the slug string with the increasing index. By default, it is set to C{"%s_%s"}.
    """

    def __init__(self, *args, **kwargs):
        self.prepopulate_from = kwargs.pop("prepopulate_from", None)
        self.unique_for_fields = kwargs.pop("unique_for_fields", [])
        return super(AutoSlugField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if not model_instance.pk:
            if self.prepopulate_from and not getattr(model_instance, self.name):
                slug = slugify(getattr(model_instance, self.prepopulate_from))
                if self.unique or len(self.unique_for_fields) > 0:
                    queryset = self._filtered_queryset(model_instance, self.unique_for_fields)
                    slug = self._unique_slug(queryset, model_instance, self.name, slug)
                setattr(model_instance, self.name, slug)
                return slug

        return super(AutoSlugField, self).pre_save(model_instance, add)

    def _filtered_queryset(self, instance, unique_for_fields):
        """ Generate a queryset filtered to be unique through all the given fields. """
        qs = instance._default_manager.all()
        for field in unique_for_fields:
            value = instance
            for part in field.split("__"):
                value = getattr(value, part)
            qs = qs.filter(**{field:value})
        return qs

    def _gen_slugs(self, value):
        """ Generate an endless stream of slugs like: "slug", "slug-1", "slug-2", ... """
        yield value
        format = setting("AUTOSLUG_FORMAT", "%s-%s")
        for i in countup():
            yield format % (value, i)

    def _unique_slug(self, queryset, instance, fieldname, value):
        """ Find a unique slug for the given queryset.  """
        for slug in self._gen_slugs(value):
            count = queryset.filter(**{fieldname:slug}).count()
            if count == 0:
                return slug
