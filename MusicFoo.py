###############################################################################
# MusicFoo.py                                                                 #
# --------------------------------------------------------------------------- #
# Description:                                                                #
#   This program aims to help with the process of maintaining a music         #
#   library. You can provide a folder structure that you prefer, naming       #
#   formats for both folders and song files of any type. Then provide a       #
#   directory containing a library of music and BAM!                          #
#                                                                             #
#   Your music library will be organized and you didn't even need to look at  #
#   it! :)                                                                    #
# --------------------------------------------------------------------------- #
# Author:                                                                     #
#   Ethan Harte                                                               #
#   Ethan.Harte@yahoo.com                                                     #
###############################################################################

import logging
import argparse

VERSION 	= "0.1.0"
VERSION_MSG = "♫ MusicFoo v{} ♫".format(VERSION)

LOG_LEVEL_NONE = 0
LOG_LEVEL_INFO = 1
LOG = logging.getLogger('♫')

def configLog(level):
    if (level == 0):
        log_level = logging.WARNING
    elif (level == 1):
        log_level = logging.INFO
    elif (level >= 2):
        log_level = logging.DEBUG
    logging.basicConfig(format='%(name)s %(asctime)s - %(levelname)s - %(message)s', level=log_level)

def parseArgs():
    parser = argparse.ArgumentParser(description='♫ MusicFoo is a tool to help organize your music library ♫')
    parser.add_argument('--library', required=True, help='Directory of unorganized music library')
    parser.add_argument('--format', required=True, help='Desired format for folders and files in music library')
    parser.add_argument('--rename_cover', required=False, action='store_true', default=False, help='If provided, all album art files will be renamed to conver.<format>')
    parser.add_argument('--require_input', required=False, action='store_true', default=False, help='If provided, the user will be asked yes(y) or no(n) for each change')
    parser.add_argument('--debug', '-d', required=False, action='count', default=0, help="Log verbosity")
    parser.add_argument('--version', '-v', action='version', version=VERSION_MSG)
    return parser.parse_args()

if __name__=="__main__":
    # Parse arguments
    args = parseArgs()

    # Configure logger
    configLog(args.debug)

    LOG.warning('Test warning')
    LOG.info('Test info')
    LOG.debug('Test debug')


# End of file