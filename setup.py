from setuptools import setup, find_packages
import regex_field
# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215_
import multiprocessing
assert multiprocessing


setup(
    name='django-regex-field',
    version=regex_field.__version__,
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
    ],
    test_suite='run_tests.run_tests',
    include_package_data=True,
)
