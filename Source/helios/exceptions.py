#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# Base class for all Helios exceptions...
class ExceptionBase(Exception):

    # Constructor...
    def __init__(self, message=None):

        # Initialize...
        self._message   = message

        # Construct base object...
        Exception.__init__(self, message)

    # Convert to an unofficial string convenience representation...
    def __str__(self):
        return self.what()

    # What is the problem as a human readable string?
    def what(self):
        return self._message


# Validation exception. This is raised if bad input was provided to the client
#  before it is submitted to the server...
class Validation(ExceptionBase):

    # Constructor...
    def __init__(self, message=None):

        # Construct base object...
        super().__init__(message)


# Connection exception. Suitable if we could not connect to the server...
class Connection(ExceptionBase):

    # Constructor...
    def __init__(self, message=None):

        # Construct base object...
        super().__init__(message)


# Helios response exception base class for all HTTP response codes...
class ResponseExceptionBase(ExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):

        # Initialize...
        self._code      = code
        self._details   = details
        self._summary   = summary

        # Construct base object...
        super().__init__(message=details)

    # What was the HTTP code?
    def get_code(self):
        return self._code

    # What are the details of the problem as a human readable string?
    def get_details(self):
        return self._details

    # What were the details of the problem as a human readable string?
    def get_summary(self):
        return self._summary


# Server provided a response, but it was not something we knew how to parse...
class UnexpectedResponse(ExceptionBase):

    # Constructor...
    def __init__(self, message=None):
        super().__init__(message)

# Bad request exception on an HTTP 400...
class BadRequest(ResponseExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Unauthorized exception on an HTTP 401...
class Unauthorized(ResponseExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Conflict exception on an HTTP 409...
class Conflict(ResponseExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Not found exception on an HTTP 404...
class NotFound(ResponseExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Internal server error exception on an HTTP 500...
class InternalServer(ResponseExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)


# Insufficient storage exception on an HTTP 507...
class InsufficientStorage(ResponseExceptionBase):

    # Constructor...
    def __init__(self, code=None, details=None, summary=None):
        super().__init__(code, details, summary)
