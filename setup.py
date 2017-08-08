#!/usr/bin/python3
# xlreg_py/setup.py

""" Setuptools project configuration for xlreg_py. """

from os.path import exists
from setuptools import setup

long_desc = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        long_desc = file.read()

setup(name='xlreg_py',
      version='0.1.25',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      long_description=long_desc,
      packages=['xlreg'],
      package_dir={'': 'src'},
      py_modules=['xlreg_client'],
      include_package_data=False,
      zip_safe=False,
      scripts=['src/xlreg_client.py'],
      description='Python 3 client for xlReg server',
      url='https://jddixon.github.io/xlreg_py',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
