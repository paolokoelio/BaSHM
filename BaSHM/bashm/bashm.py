#!/usr/bin/env python
# encoding: utf-8
'''
bashm.bashm -- main of the program

bashm.bashm starts a menu for program flow actions

It defines main + some error control (and logging TODO)

@author:     koelio

@copyright:  2017 unipv. All rights reserved.

@license:    CC

@contact:    paolokoelio@gmail.com
@deffield    updated: 23/11
'''

import sys, traceback
import os

from menu import Menu
from optparse import OptionParser
import ConfigParser  # import not compatible with python3, should be configparser


__all__ = []
__version__ = 0.1
__date__ = '2017-10-23'
__updated__ = '2017-11-24'
__config = None
CONFIG_PATH = '..\config\config.cfg'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1.01"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2017 Pavlo Burda (UNIPV)                                            \
                Licensed under the Creative Commons"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False,
                          help="set recursive option for timeline extraction")
#         parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
#         parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")

        # set defaults
#         parser.set_defaults(recursive=Fase)

        #initialize configuration from file
        __config = init_config()

        # process options
        (opts, args) = parser.parse_args(argv)
#         opts = parser.parse_args()

#         if opts.verbose > 0:
#             print("verbosity level = %d" % opts.verbose)
        if opts.recursive:
            #the -r option works only for TSK modules (i.e. not for super-timeline, that is recursive by default)
            print("recursive = %s" % opts.recursive)
            __config.set('functionalities', 'recursive', 'true')
            
#         if opts.outfile:
#             print("outfile = %s" % opts.outfile)




#         Launch main menu
        print("Welcome to BaHSM\n")
        
        menu = Menu(__config)
        menu.set_options(False) # future work
        menu.main_menu()
#       #  test
#         from partitions.Partitions import Partitions
#         from extractor.TSKExtractor import TSKExtractor #test
#         e = TSKExtractor(Partitions())
#         e.TSKtimel()

        print("Exiting correctly.")


    except Exception as e:
        traceback.print_exc()
        #indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        #sys.stderr.write(indent + "  for help use --help\n")
        
        return 2

def init_config():
  try:
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_PATH)
    return config
  except Exception as e:
    sys.stderr.write(repr(e) + " in config file. at " + CONFIG_PATH + "\n")
    traceback.print_exc()


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'bashm.bashm_profile.txt'
        cProfile.mmls('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())