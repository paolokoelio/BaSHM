#!/usr/bin/env python
# encoding: utf-8
'''
bashm.bashm -- main of the program

bashm.bashm starts a menu for program flow actions

It defines main + some error control (and logging TODO)

@author:     koelio

@copyright:  2017 University of Pavia . All rights reserved.

@license:    Creative Commons Attribuzione 4.0 Internazionale

@contact:    paolokoelio@gmail.com
@deffield    updated: 12/12
'''

import sys, traceback
import os

from menu import Menu
from optparse import OptionParser
import ConfigParser


__all__ = []
__version__ = 0.1
__date__ = '2017-12-15'
__updated__ = '2017-12-12'
__config = None
# configuration path of the main modules, refer to the README for a description
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
        parser.add_option("-n", "--non-recursive", dest="recursive", action="store_true", default=False,
                          help="un-set recursiveness option for timeline extraction")

        #initialize configuration from file
        __config = init_config()

        # process options
        (opts, args) = parser.parse_args(argv)

        if opts.recursive:
            #the -r option works only for TSK modules (i.e. not for super-timeline, that is recursive by default)
            print("non-recursive = %s" % opts.recursive)
            __config.set('functionalities', 'recursive', 'false')

#         Launch main menu
        print("Welcome to BaHSM\n")
        

        menu = Menu(__config)
        menu.main_menu()

        print("Exiting correctly.")


    except Exception as e:
        traceback.print_exc()
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        
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