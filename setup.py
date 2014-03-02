import os
from setuptools import setup


setup(
    name='django-regex-field',
    version=open(os.path.join(os.path.dirname(__file__), 'regex_field', 'VERSION')).read().strip(),
    description='Store regular expressions in Django models',
    long_description=open('README.md').read(),
    url='http://github.com/ambitioninc/django-regex-field/',
    author='Wes Kendall',
    author_email='wesleykendall@gmail.com',
    packages=[
        'regex_field',
    ],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    install_requires=[
        'django>=1.4',
    ],
    include_package_data=True,
)
