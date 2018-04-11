[![Build Status](https://travis-ci.org/ambitioninc/django-regex-field.png)](https://travis-ci.org/ambitioninc/django-regex-field)

# django-regex-field

Stores regular expressions in Django models.

## A Brief Overview
The Django regex field app provides a custom field for a Django model that
stores a regex. This provides the ability to easily store regexs and access
them as compiled regular expressions from your models.


## Storing and Retrieving a Regex
A regular expression can be stored and retrieved in a Django model as follows:
```python
from django.db import models
from regex_field.fields import RegexField


class RegexModel(models.Model):
    regex = RegexField(max_length=128)


model_obj = RegexModel.objects.create(regex='a')

# Access the regex as a compiled regular expression
>>> print(model_obj.regex.match('b'))
None

## Using regex flags
Flags can be provided in the field definition and will be applied when the regex is compiled. If you manually
compile a regex object with other flags and set it on the model, those flags will not be preserved. Only the flags
passed to the field's constructor are used.
```python
import re
from django.db import models
from regex_field.fields import RegexField


class RegexModel(models.Model):
    regex = RegexField(max_length=128, re_flags=re.IGNORECASE)


model_obj = RegexModel.objects.create(regex='A')

# Case insensitive matching
>>> print(model_obj.regex.match('a') is not None)
True

```
