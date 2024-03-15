#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# i18n...
import gettext
_ = gettext.gettext

# Chunked upload class to allow file upload progress with Requests library...
class chunked_upload:

    # Constructor takes data, size of chunk on each read, and a progress
    #  callback of the from foo(bytes_read, new_bytes, total_bytes)
    def __init__(self, data, chunk_size=8096, progress_callback=None):

        # Initialize...
        self._data              = data
        self._chunk_size        = chunk_size
        self._total_size        = len(data)
        self._bytes_read        = 0
        self._progress_callback = progress_callback

    # Iterator method...
    def __iter__(self):

        # Keep reading data for caller until no more...
        while self._bytes_read < self._total_size:

            # Read a chunk...
            chunk = self._data[self._bytes_read:self._bytes_read + self._chunk_size]

            # Update read pointer...
            self._bytes_read += len(chunk)

            # If a progress callback was provided, invoke it...
            if self._progress_callback:
                self._progress_callback(
                    self._bytes_read, len(chunk), self._total_size)

            # Return generator for caller of read data...
            yield chunk

    # Length of upload...
    def __len__(self):
        return self._total_size
