#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
import os
import sys
import requests

# i18n...
import gettext
_ = gettext.gettext

# Chunked upload class to allow file upload progress with Requests library...
class chunked_upload(object):

    # Constructor takes a filename and size of chunk...
    def __init__(self, filename, chunk_size=8096):

        # Initialize...
        self._filename      = filename
        self._chunk_size    = chunk_size
        self._total_size    = os.path.getsize(filename)
        self._bytes_read    = 0

    # Iterator method...
    def __iter__(self):

        # Open the file and keep reading data for caller until done...
        with open(self._filename, 'rb') as file:
            while True:

                # Read a chunk...
                data = file.read(self._chunk_size)

                # No more data left...
                if not data:
                    break

                # Update read pointer...
                self._bytes_read += len(data)

                # Return generator for caller...
                yield

    # Length of upload...
    def __len__(self):
        return self._total_size

