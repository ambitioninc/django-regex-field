from django.db import models

from regex_field import RegexField


class RegexModel(models.Model):
    """
    A model for testing saving and compiling of regexs.
    """
    regex = RegexField(max_length=128)


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
