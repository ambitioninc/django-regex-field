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
from regex_field import RegexField


class RegexModel(models.Model):
    regex = RegexField(max_length=128)


model_obj = RegexModel.objects.create(regex='a')

# Access the regex as a compiled regular expression
>>> print(model_obj.regex.match('b'))
None
```
