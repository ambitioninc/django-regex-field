import re

from django.core.exceptions import ValidationError
from django.core.management import call_command
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
        self.assertIsNotNone(test_obj.regex.match('a'))
        self.assertIsNone(test_obj.regex.match('b'))

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

    def test_validators(self):
        """
        Run clean_fields to catch validator issues
        """
        regex_model = RegexModel(with_validator='12345')
        with self.assertRaises(ValidationError):
            regex_model.clean_fields()

        regex_model = RegexModel(with_validator='1234')
        regex_model.clean_fields()
        regex_model.save()

    def test_dumpdata(self):
        """
        Make sure django can serializer the model
        """
        regex_model = RegexModel(with_validator='1234')
        regex_model.clean_fields()
        regex_model.save()

        call_command('dumpdata')

    def test_loaddata(self):
        """
        Make sure django can deserialize the model
        """
        call_command('loaddata', 'data.json')

        regex_model = RegexModel.objects.get()
        self.assertEqual(regex_model.with_validator.pattern, '1234')

    def test_re_flags(self):
        """
        Apply re options when being created
        """
        regex_model = RegexModel(regex='ABcd', with_options='ABcd')

        # Test case sensitive field
        self.assertIsNone(regex_model.regex.match('abcd'))
        self.assertIsNotNone(regex_model.regex.match('ABcd'))

        # Test case insensitive field
        self.assertIsNotNone(regex_model.with_options.match('ABcd'))
        self.assertIsNotNone(regex_model.with_options.match('abcd'))
        self.assertIsNotNone(regex_model.with_options.match('abCD'))

        # Save the model to the db
        regex_model.save()

        # Reload the model and check that the flags are still respected
        regex_model = RegexModel.objects.get(id=regex_model.id)

        # Test case sensitive field
        self.assertIsNone(regex_model.regex.match('abcd'))
        self.assertIsNotNone(regex_model.regex.match('ABcd'))
        self.assertIsNotNone(regex_model.regex.match('ABcd'))

        # Test case insensitive field
        self.assertIsNotNone(regex_model.with_options.match('ABcd'))
        self.assertIsNotNone(regex_model.with_options.match('abcd'))
        self.assertIsNotNone(regex_model.with_options.match('abCD'))
