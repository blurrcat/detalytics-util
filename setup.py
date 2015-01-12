#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This package can be installed with only the necessary dependencies for
features. Features:
 * celery
 * notification

To only use the notification feature, install as follows::

    pip install util[notification]
    pip install -e .[notification]


"""
from setuptools import setup, find_packages

__version__ = '0.3.0'
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


feature_requires = {
    'celery': [
        'celery',
        'raven',
    ],
    'notification': [
        'twilio',
        'Flask-Mail',
        'redis',
    ]
}
install_requires = [
    'Flask',
]
tests_require = install_requires + feature_requires.values() + [
    'pytest==2.5.1', 'pytest-cov==1.6', 'mock==1.0.1']
develop_require = tests_require + [
    'Sphinx>=1.2.1', 'pylint>=1.1.0']

extra_requires = {
    'develop': develop_require,
    'test': tests_require,
}
extra_requires.update(feature_requires)

setup(
    name='util',
    version=__version__,
    description='common utilities',
    long_description=readme + '\n\n' + history,
    author='Try Again Concepts',
    author_email='',
    url='https://github.com/tryagainconepts/util',
    packages=find_packages(),
    package_dir={'util': 'util'},
    install_requires=install_requires,
    extras_require=extra_requires,
    zip_safe=False,
    keywords='util',
)
