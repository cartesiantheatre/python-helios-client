#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Helios exception base class...
class HeliosExceptionBase(Exception):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):

        # Initialize...
        self._code      = code
        self._details   = details
        self._summary   = summary

        # Construct base object...
        Exception.__init__(self, summary)

    # What are the details of the problem as a human readable string?
    def get_details(self):
        return self._details

    # What were the details of the problem as a human readable string?
    def get_summary(self):
        return self._summary


# Bad request exception. Suitable on a 400...
class BadRequest(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Unauthorized exception. Suitable on a 401...
class Unauthorized(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Not found exception. Suitable on a 404...
class NotFound(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Internal server error exception. Suitable on a 500...
class InternalServer(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Insufficient storage exception. Suitable on a 507...
class InsufficientStorage(HeliosExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


