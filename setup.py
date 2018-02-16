#!/usr/bin/python3
# xlreg_py/setup.py

""" Setuptools project configuration for xlreg_py. """

from os.path import exists
from setuptools import setup

LONG_DESC = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        LONG_DESC = file.read()

setup(name='xlreg_py',
      version='0.1.30',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      long_description=LONG_DESC,
      packages=['xlreg'],
      package_dir={'': 'src'},
      py_modules=['xlreg_client'],
      include_package_data=False,
      zip_safe=False,
      scripts=['src/xlreg_client.py'],
      ext_modules=[],
      description='Python 3 client for xlReg server',
      url='https://jddixon.github.io/xlreg_py',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 2.7',
          'Programming Language :: Python 3.3',
          'Programming Language :: Python 3.4',
          'Programming Language :: Python 3.5',
          'Programming Language :: Python 3.6',
          'Programming Language :: Python 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
