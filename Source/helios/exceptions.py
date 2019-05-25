#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Helios exception base class...
class HeliosExceptionBase(Exception):

    # Constructor...
    def __init__(self, code=None, message=None):

        # Initialize...
        self._code      = code
        self._message   = message

        # Construct base object...
        Exception.__init__(self, message)

    # What was the problem as a human readable string?
    def what(self):
        return self._message

# A problem occured during input or output. Suitable for timeouts or if the host
#  could not be reached...
class ConnectionError(HeliosExceptionBase):

    # Constructor...
    def __init__(self, message=None):
        HeliosExceptionBase.__init__(self, code=None, message=None)

# Bad request exception. Suitable on a 400...
class BadRequest(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=400, message=None):
        HeliosExceptionBase.__init__(self, code, message)

# Unauthorized exception. Suitable on a 401...
class Unauthorized(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=401, message=None):
        HeliosExceptionBase.__init__(self, code, message)

# Not found exception. Suitable on a 404...
class NotFound(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=404, message=None):
        HeliosExceptionBase.__init__(self, code, message)

# Internal server error exception. Suitable on a 500...
class InternalServer(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=500, message=None):
        HeliosExceptionBase.__init__(self, code, message)

# Insufficient storage exception. Suitable on a 507...
class InsufficientStorage(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=507, message=None):
        HeliosExceptionBase.__init__(self, code, message)

