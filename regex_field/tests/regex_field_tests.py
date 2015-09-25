import re

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import RegexModel, BlankTrueModel, NullTrueModel


class RegexFieldTest(TestCase):
    """
    Tests storing and calling functions/classes that are stored in test models.
    """
    def test_blank(self):
        """
        Tests that blank regexs can be saved with blank=True.
        """
        test_obj = BlankTrueModel.objects.create(regex='')
        self.assertEqual(test_obj.regex, re.compile(''))

    def test_null(self):
        """
        Tests that null regexs can be saved with null=True.
        """
        test_obj = NullTrueModel.objects.create(regex=None)
        self.assertEqual(test_obj.regex, None)
        test_obj = NullTrueModel.objects.get(id=test_obj.id)
        self.assertEqual(test_obj.regex, None)

    def test_save_str(self):
        """
        Tests that regex strings are saved and accessed properly.
        """
        test_obj = RegexModel.objects.create(regex='a')
        self.assertNotEqual(test_obj.regex.match('a'), None)
        self.assertEqual(test_obj.regex.match('b'), None)

        # Set the value of the test obj and call save. Verify the function can still be loaded properly
        test_obj.regex = 'z'
        test_obj.save()
        test_obj = RegexModel.objects.get(id=test_obj.id)
        self.assertNotEqual(test_obj.regex.match('z'), None)
        self.assertEqual(test_obj.regex.match('b'), None)

    def test_save_regex(self):
        """
        Tests that compiled regexs can be saved and accessed.
        """
        regex = re.compile('a')
        test_obj = RegexModel.objects.create(regex=regex)
        self.assertNotEqual(test_obj.regex.match('a'), None)
        self.assertEqual(test_obj.regex.match('b'), None)

        # Set the value of the test obj and call save. Verify the function can still be loaded properly
        test_obj.regex = re.compile('z')
        test_obj.save()
        test_obj = RegexModel.objects.get(id=test_obj.id)
        self.assertNotEqual(test_obj.regex.match('z'), None)
        self.assertEqual(test_obj.regex.match('b'), None)

    def test_invalid_regex(self):
        """
        Tests accessing an invalid regex.
        """
        with self.assertRaises(ValidationError):
            RegexModel.objects.create(regex='he(lo')
