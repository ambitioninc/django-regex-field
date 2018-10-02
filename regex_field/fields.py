import re

from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.fields import CharField


class CastOnAssignDescriptor(object):
    """
    A property descriptor which ensures that `field.to_python()` is called on _every_ assignment to the field.
    This used to be provided by the `django.db.models.subclassing.Creator` class, which in turn
    was used by the deprecated-in-Django-1.10 `SubfieldBase` class, hence the reimplementation here.
    Copied from https://stackoverflow.com/questions/
    39392343/how-do-i-make-a-custom-model-field-call-to-python-when-the-field-is-accessed-imm
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:  # pragma: no cover
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class RegexField(CharField):
    """
    A field that stores a regular expression and compiles it when accessed.
    """
    description = 'A regular expression'
    # Maintain a cache of compiled regexs for faster lookup
    compiled_regex_cache = {}

    def __init__(self, *args, **kwargs):
        self.re_flags = kwargs.pop('re_flags', None)
        super(RegexField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = self.to_python(value)
        return self.value_to_string(value)

    def get_cache_key(self, value, flags):
        return 'value-{0}-flags-{1}'.format(value, flags)

    def get_compiled_regex(self, value):
        cache_key = self.get_cache_key(value, self.re_flags)
        if cache_key not in self.compiled_regex_cache:
            if self.re_flags is None:
                self.compiled_regex_cache[cache_key] = re.compile(value)
            else:
                self.compiled_regex_cache[cache_key] = re.compile(value, flags=self.re_flags)
        return self.compiled_regex_cache[cache_key]

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def contribute_to_class(self, cls, name, virtual_only=False):
        """
        Cast to the correct value every
        """
        super(RegexField, self).contribute_to_class(cls, name, virtual_only)
        setattr(cls, name, CastOnAssignDescriptor(self))

    def to_python(self, value):
        """
        Handles the following cases:
        1. If the value is already the proper type (a regex), return it.
        2. If the value is a string, compile and return the regex.

        Raises: A ValidationError if the regex cannot be compiled.
        """
        if isinstance(value, type(re.compile(''))):
            return value
        else:
            if value is None and self.null:
                return None
            else:
                try:
                    return self.get_compiled_regex(value)
                except:
                    raise ValidationError('Invalid regex {0}'.format(value))

    def value_to_string(self, obj):
        # Return None if obj is None
        if obj is None:
            return None

        # Django passes a model instead of the value when serializing for dumpdata
        if issubclass(obj.__class__, Model):
            obj = self.value_from_object(obj)

        # Check for re type before accessing pattern
        if isinstance(obj, re.Pattern):
            return obj.pattern

        # Return None by default
        return None

    def run_validators(self, value):
        """
        Make sure value is a string so it can run through django validators
        """
        value = self.to_python(value)
        value = self.value_to_string(value)
        return super(RegexField, self).run_validators(value)
