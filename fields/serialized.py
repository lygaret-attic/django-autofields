from django.db.models.fields import TextField
from django.db.models import SubfieldBase
import pickle, base64

class SerializedDataField(TextField):
    """
    A field which serializes python values to the database, and returns
    them intact.
    """
    __metaclass__ = SubfieldBase

    def to_python(self, value):
        if value is None or value is "": return
        if not isinstance(value, basestring): return value
        try:
            return pickle.loads(base64.b64decode(value))
        except:
            return

    def get_db_prep_save(self, value):
        if value is None or value is "": return
        return base64.b64encode(pickle.dumps(value))
