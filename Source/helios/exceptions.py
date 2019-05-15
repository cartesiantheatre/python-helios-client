#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Helios exception base class...
class HeliosExceptionBase(Exception):

    # Constructor...
    def __init__(self, Code=None, Message=None):

        # Initialize...
        self._Code      = Code

        # Construct base object...
        Exception.__init__(self, Message)

# A problem occured during input or output. Suitable for timeouts or if the host
#  could not be reached...
class IOError(HeliosExceptionBase):

    # Constructor...
    def __init__(self, Message=None):
        HeliosExceptionBase.__init__(self, Code=None, Message=None)

# Bad request exception. Suitable on a 400...
class BadRequest(HeliosExceptionBase):

    # Constructor...
    def __init__(self, Code=400, Message=None):
        HeliosExceptionBase.__init__(self, Code, Message)

# Unauthorized exception. Suitable on a 401...
class Unauthorized(HeliosExceptionBase):

    # Constructor...
    def __init__(self, Code=401, Message=None):
        HeliosExceptionBase.__init__(self, Code, Message)

# Not found exception. Suitable on a 404...
class NotFound(HeliosExceptionBase):

    # Constructor...
    def __init__(self, Code=404, Message=None):
        HeliosExceptionBase.__init__(self, Code, Message)

# Internal server error exception. Suitable on a 500...
class InternalServer(HeliosExceptionBase):

    # Constructor...
    def __init__(self, Code=500, Message=None):
        HeliosExceptionBase.__init__(self, Code, Message)

# Insufficient storage exception. Suitable on a 507...
class InsufficientStorage(HeliosExceptionBase):

    # Constructor...
    def __init__(self, Code=507, Message=None):
        HeliosExceptionBase.__init__(self, Code, Message)

