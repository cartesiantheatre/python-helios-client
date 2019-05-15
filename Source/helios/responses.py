#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
from collections import namedtuple

# Response after adding or retrieving a song...
StoredSongResponse = namedtuple('StoredSongResponse',
[
    'album',
    'algorithm_age',
    'artist',
    'duration',
    'genre',
    'id',
    'isrc',
    'location',
    'reference',
    'title',
    'year'
])

# Response after server produces an error...
ErrorResponse = namedtuple('ErrorResponse',
[
    'code',
    'details',
    'summary'
])

# Disk field of response on server status request...
ServerDiskStatusResponse = namedtuple('ServerDiskStatusResponse',
[
    'client_store_upload',
    'client_store_upload_directory',
    'available',
    'capacity'
])

# Response on status request...
ServerStatusResponse = namedtuple('ServerStatusResponse',
[
    'server_status',
    'built',
    'disk',
    'configured',
    'encoding',
    'songs',
    'system',
    'uptime',
    'version'
])

