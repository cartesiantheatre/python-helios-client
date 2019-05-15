#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
from collections import namedtuple

# i18n...
import gettext
_ = gettext.gettext

# New song...
NewSong = namedtuple('NewSong',
[
    'album',
    'artist',
    'file',
    'genre',
    'isrc',
    'reference',
    'title',
    'year'
])

# An object suitable for modifying an existing song...
PatchSong = namedtuple('PatchSong',
[
    'album',
    'artist',
    'file',
    'genre',
    'isrc',
    'reference',
    'title',
    'year'
])

