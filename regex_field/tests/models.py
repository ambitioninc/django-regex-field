from django.core.validators import MaxLengthValidator
from django.db import models

from regex_field.fields import RegexField


class RegexModel(models.Model):
    """
    A model for testing saving and compiling of regexs.
    """
    regex = RegexField(max_length=128)
    with_validator = RegexField(max_length=128, validators=[MaxLengthValidator(4)])


class BlankTrueModel(models.Model):
    """
    A model with a blank=True RegexField.
    """
    regex = RegexField(blank=True, max_length=128)


class NullTrueModel(models.Model):
    """
    A model with a null=True RegexField.
    """
    regex = RegexField(null=True, max_length=128)
