from django.db.models.fields import TextField
from django.conf import settings
from markdown import markdown

class AutoMarkdownTextField(TextField):
    """
    A field which auto populates with the value of the given field,
    processed through markdown.
    """
    def __init__(self, *args, **kwargs):
        self.prepopulate_from = kwargs.pop("prepopulate_from", None)
        self.only_on_create = kwargs.pop("only_on_create", False)
        return super(AutoMarkdownTextField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.prepopulate_from and not (self.only_on_create and model_instance.pk):
            base = getattr(model_instance, self.prepopulate_from)
            text = markdown(base, getattr(settings, "AUTOMARKDOWN_EXTENSIONS", []))
            setattr(model_instance, self.name, text)
            return text
        else:
            return super(AutoMarkdownTextField, self).pre_save(model_instance, add)
