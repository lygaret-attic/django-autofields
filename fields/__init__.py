def setting(name, default=None):
    if hasattr(settings, name):
        return getattr(settings, name)
    return default

from autoslug import *
from automarkdown import *
from serialized import *

__all__ = [AutoSlugField, AutoMarkdownTextField, SerializedDataField]
