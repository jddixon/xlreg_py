#!/usr/bin/python3

# ~/dev/py/xlreg_py/xlRegClient.py

import os
import re
import sys
import time
from argparse import ArgumentParser

from xlattice.util import DecimalVersion, parseDecimalVersion
from xlReg import *    # REPLACE WITH SPECIFICS

# -- implementation -------------------------------------------------


def doClientSTuff(options):
    dontDoIt = options.dontDoIt
    verbose = options.verbose


def main():

    # program defaults ----------------------------------------------
    today = time.localtime(time.time())    # struct time
    newDate = '%4d-%02d-%02d' % (today.tm_year,
                                 today.tm_mon,
                                 today.tm_mday)

    # parse the command line ----------------------------------------
    parser = ArgumentParser(description='example xlReg client')

    parser.add_argument('-j', '--justShow', action='store_true',
                        help='show options and exit')

    parser.add_argument('-T', '--testing', action='store_true',
                        help='this is a test run')

    parser.add_argument('-V', '--showVersion', action='store_true',
                        help='specify actual new version number')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='be chatty')

    parser.add_argument('-z', '--dontDoIt', action='store_true',
                        help='just say what you would do')

    args = parser.parse_args()

    # fixups with sanity checks -------------------------------------

    # fixups --------------------------------------------------------

    # sanity checks -------------------------------------------------

    # complete setup ------------------------------------------------
    appName = 'xlRegClient.py %s' % __version__

    # maybe show options and such -----------------------------------
    if args.verbose or args.justShow or args.showVersion:
        print("%s %s" % (appName, __version_date__))

    if args.showVersion:
        sys.exit(0)

    if args.verbose or args.justShow:
        print('dontDoIt         = ' + str(args.dontDoIt))
        print('showVersion      = %s' % args.showVersion)
        print('testing          = ' + str(args.testing))
        print('verbose          = ' + str(args.verbose))

    if args.justShow:
        sys.exit(0)

    # do what's required --------------------------------------------
    doClientSTuff(args)

if __name__ == '__main__':
    main()
