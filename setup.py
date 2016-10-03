#!/usr/bin/python3
# ~/dev/py/xlreg/setup.py

""" Set up the Python xlReg client. """

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('xlreg/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='xlreg_py',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      #
      # wherever we have a .py file that will be imported, we
      # list it here, without the .py extension but SQuoted
      py_modules=[],
      #
      # ftlog is not a package because it doesn't have its own
      # subdir and __init__.py
      packages=['xlreg', ],
      #
      # following could be in scripts/ subdir; SQuote
      scripts=['xlreg_client.py'],
      description='Python 3 client for xlReg server',
      url='https://jddixon/github.io/xlreg_py',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
