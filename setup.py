#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="Pytoad",
      version="1.0.3",
      description="Pytoad is a lightweight Hoptoad notifier for Python.",
      author="Benjamin Coe",
      author_email="ben@attachments.me",
      entry_points = {},
      url="https://github.com/attachmentsme/Pytoad",
      packages = find_packages(),
      install_requires = ['xmlbuilder', 'simplejson'],
      tests_require=['nose', 'coverage', 'mock']
)
