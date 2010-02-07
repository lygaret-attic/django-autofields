from autoslug import *
from automarkdown import *
from serialized import *

__all__ = [AutoSlugField, AutoMarkdownTextField, SerializedDataField]


# custom south stuff
try:
	from south.modelsinspector import add_introspection_rules
	rules = [
		(
			(AutoSlugField, ),
			[],
			{
				"prepopulate_from": ["prepopulate_from", {"default": None}],
				"unique_for_fields": ["unique_for_fields", {"default": []}],
			}
		),
		(
			(AutoMarkdownTextField, ),
			[],
			{
				"prepopulate_from": ["prepopulate_from", {"default": None}],
				"only_on_create": ["only_on_create", {"default": False}],
			}
		),
		(
			(SerializedDataField, ), [], {}
		),
	]

	add_introspection_rules(rules, ["^autofields"])
except ImportError:
	pass
