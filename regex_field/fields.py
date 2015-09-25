import re

from six import add_metaclass

from django.core.exceptions import ValidationError
from django.db.models import SubfieldBase
from django.db.models.fields import CharField


@add_metaclass(SubfieldBase)
class RegexField(CharField):
    """
    A field that stores a regular expression and compiles it when accessed.
    """
    description = 'A regular expression'
    # Maintain a cache of compiled regexs for faster lookup
    compiled_regex_cache = {}

    def get_prep_value(self, value):
        value = self.to_python(value)
        return self.value_to_string(value)

    def get_compiled_regex(self, value):
        if value not in self.compiled_regex_cache:
            self.compiled_regex_cache[value] = re.compile(value)
        return self.compiled_regex_cache[value]

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
        if obj is None:
            return None
        else:
            return obj.pattern
