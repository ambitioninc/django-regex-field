# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215_
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'regex_field/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='django-regex-field',
    version=get_version(),
    description='Store regular expressions in Django models',
    long_description=open('README.md').read(),
    url='http://github.com/ambitioninc/django-regex-field/',
    author='Wes Kendall',
    author_email='wesleykendall@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    install_requires=[
        'django>=1.4',
    ],
    tests_require=[
        'psycopg2',
        'django-nose',
        'south',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
)
