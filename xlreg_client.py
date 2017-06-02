#!/usr/bin/python3
# ~/dev/py/xlreg_py/xlRegClient.py

""" Module for python xlReg client. """

import sys
import time
from argparse import ArgumentParser

# from xlattice.util import DecimalVersion, parseDecimalVersion
from xlreg import __version__, __version_date__

# -- implementation -------------------------------------------------


def do_client_stuff(options):
    """ STUB for what the client needs to do. """
    pass


def main():
    """ Entry point for xlReg client program. """

    # program defaults ----------------------------------------------
    today = time.localtime(time.time())    # struct time
    new_date = '%4d-%02d-%02d' % (today.tm_year,
                                  today.tm_mon,
                                  today.tm_mday)

    # parse the command line ----------------------------------------
    parser = ArgumentParser(description='example xlReg client')

    parser.add_argument('-j', '--just_show', action='store_true',
                        help='show options and exit')

    parser.add_argument('-T', '--testing', action='store_true',
                        help='this is a test run')

    parser.add_argument('-V', '--show_version', action='store_true',
                        help='specify actual new version number')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='be chatty')

    parser.add_argument('-z', '--dont_do_it', action='store_true',
                        help='just say what you would do')

    args = parser.parse_args()

    # fixups with sanity checks -------------------------------------

    # fixups --------------------------------------------------------

    # sanity checks -------------------------------------------------

    # complete setup ------------------------------------------------
    app_name = 'xlreg_client.py %s' % __version__

    # maybe show options and such -----------------------------------
    if args.verbose or args.just_show or args.show_version:
        print("%s %s" % (app_name, __version_date__))

    if args.show_version:
        sys.exit(0)

    if args.verbose or args.just_show:
        print('dont_do_it         = ' + str(args.dont_do_it))
        print('show_version      = %s' % args.show_version)
        print('testing          = ' + str(args.testing))
        print('verbose          = ' + str(args.verbose))

    if args.just_show:
        sys.exit(0)

    # do what's required --------------------------------------------
    do_client_stuff(args)


if __name__ == '__main__':
    main()
