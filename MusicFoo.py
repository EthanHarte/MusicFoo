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
import os
import json
from functools import reduce

VERSION     = "0.1.0"
VERSION_MSG = "♫ MusicFoo v{} ♫".format(VERSION)

LOG_LEVEL_NONE = 0
LOG_LEVEL_INFO = 1
LOG = logging.getLogger('♫')

# MF_Library defines a music library
class MF_Library:
    library_path    =''
    library_format  ='<Artist>/<Album>/<Track>'
    library         = {}
    artists         = []
    rename_cover    = 0
    require_input   = 0

    def __init__(self, _path, _format, _rename_cover=0, _require_input=0):
        _path = os.path.normpath(_path)
        LOG.debug(_path)
        if (os.path.isdir(_path) == False):
            LOG.warning("Directory {} does not exist".format(_path))
            exit()
        self.library_path = _path
        self.library_format = _format # TODO: implement library format
        self.rename_cover = _rename_cover
        self.require_input = _require_input
        self.loadLibrary()
        self.loadArtists()
        self.printLibrary()
        self.printArtists()

    # Loads the music library found at the library_path into a nested dictionary.
    # TODO: load the library based on the library format
    def loadLibrary(self):
        LOG.info("Loading library...")

        rootdir = self.library_path.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        LOG.debug(rootdir)
        LOG.debug(start)
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = reduce(dict.get, folders[:-1], self.library)
            parent[folders[-1]] = subdir

        # Remove the root folder from the library dictionary
        self.library = self.library[os.path.basename(rootdir)]

    # Loads the artists from the library dict into an artists list
    def loadArtists(self):
        LOG.info("Loading Artists...")
        self.artists = list(self.library.keys())

    # Print the library dictionary in pretty JSON format
    def printLibrary(self):
        LOG.debug("Library:\n" + json.dumps(self.library, indent=4, sort_keys=True))

    # Print artists list
    def printArtists(self):
        LOG.debug("Artists:\n" + str(self.artists))

    # Given an artist, return a list of that artist's albums
    def getAlbums(self, artist):
        LOG.info("Getting albums for {}".format(artist))
        return list(self.library.get(artist).keys())

    # Given an artists and an album, return the tracks for that album.
    # Requires artist since multiple artists might have the same album title.
    # TODO: Filter out non-tracks by looking at file type. Don't want to return a .jpg as a track.
    def getTracks(self, artist, album):
        LOG.info("Getting tracks for {} - {}".format(artist, album))
        if (os.path.isdir(os.path.join(self.library_path, artist, album)) == False):
            LOG.warning("Album {} is not a folder".format(album))
            return []
        return list(self.library[artist][album].keys())

    def getAlbumArt(self, artist, album):
        LOG.info("Searching for album art for {} - {}".format(artist, album))

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

    lib = MF_Library(args.library, args.format)
    for artist in lib.artists:
        albums = lib.getAlbums(artist)
        LOG.debug(albums)
        for album in albums:
            tracks = lib.getTracks(artist, album)
            LOG.debug(tracks)

# End of file