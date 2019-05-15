#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
import os
import sys
import requests
import json
from helios.exceptions import *
from helios.responses import *

# i18n...
import gettext
_ = gettext.gettext

def foo():
    print('blah')

# Class to handle all client communication with a Helios server...
class client(object):

    # Class attribute for JSON MIME type...
    _JSONMimeType  = 'application/json'

    # Constructor...
    def __init__(self, Token, Host, Port=6440, Version='v1'):

        # Initialize...
        self._Token     = Token
        self._Host      = Host
        self._Port      = Port
        self._Version   = Version

    # Add a new song to your music catalogue...
    def addSong(self, Store=True, NewSong=dict()):

        # Initialize headers...
        Headers = {}
        Headers['X-API-Token']  = self._Token
        Headers['Accept']       = client._JSONMimeType
        Headers['Content-Type'] = client._JSONMimeType

        # Prepare request...
        Response = requests.post(
            self._getURL('/songs'),
            params={'store': str(Store).lower()},
            headers=Headers,
            json=NewSong)

        # Check response OK...
        self._submitRequest(Response, 201)

        # Retrieve JSON body...
        JSONResponse = Response.json()

        # Return constructed stored song from response...
        return responses.StoredSongResponse(
            album=JSONResponse['album'],
            algorithm_age=int(JSONResponse['algorithm_age']),
            artist=JSONResponse['artist'],
            duration=int(JSONResponse['duration']),
            genre=JSONResponse['genre'],
            id=int(JSONResponse['id']),
            isrc=JSONResponse['isrc'],
            location=JSONResponse['location'],
            reference=JSONResponse['reference'],
            title=JSONResponse['title'],
            year=int(JSONResponse['year']))

    # Check to ensure an HTTP response was as expected, and if not, to raise an
    #  appropriate exception...
    def _submitRequest(self,  Endpoint, Method, Headers=dict()):

        # Get the base URL...
        URL = self._getURL(Endpoint)

        # Try to submit request to server using appropriate HTTP verb...
        try:

            # Perform GET request if requested...
            if Method == 'GET':
                Response = requests.get(URL, headers=Headers)

        # Connection timeout or bad host...
        except (requests.ConnectionError, requests.Timeout) as SomeException:
            raise exceptions.IOError() from SomeException

        # Found host, but it's rejecting our connection request...
        except ConnectionRefusedError as SomeException:
            raise exception.IOError() from SomeException

        # We reached the server. If we didn't get an expected response, raise an
        #  exception...
        try:
            Response.raise_for_status()

        # Server or something in between reported an error...
        except Exception as SomeException:

            # Get the response body...
            JSONResponse = SomeException.response.json()
            Error = responses.ErrorResponse(
                code=int(JSONResponse['code']),
                details=JSONResponse['details'],
                summary=JSONResponse['summary'])

            # Bad request exception. Suitable on a 400...
            if Code is 400:
                raise BadRequest(Error.details, Error.summary)

            # Unauthorized exception. Suitable on a 401...
            elif Code is 401:
                raise Unauthorized(Error.details, Error.summary)

            # Not found exception. Suitable on a 404...
            elif Code is 404:
                raise NotFound(Error.details, Error.summary)

            # Internal server error exception. Suitable on a 500...
            elif Code is 500:
                raise InternalServer(Error.details, Error.summary)

            # Insufficient storage exception. Suitable on a 507...
            elif Code is 507:
                raise InsufficientStorage(Error.details, Error.summary)

            # Some other code...
            else:
                raise

        # Return the response object...
        return Response

    # Delete a song or songs by their ID...
    def deleteSongsByID(self):
        pass

    # Delete songs by their reference...
    def deleteSongsByReference(self):
        pass

    # Retrieve a list of all songs...
    def getAllSongs(self):
        pass

    # Search for a similar song or songs...
    def getSimilarSongs(self):
        pass

    # Retrieve a song or songs by their IDs...
    def getSongsById(self, SongID):
        return requests.get(self._getURL('/songs/by_id/{:d}/'.format(SongID)), headers={'Accept': 'application/json'})

    # Get server information status as JSON...
    def getServerStatus(self):

        # Initialize headers...
        Headers = {}
        Headers['X-API-Token']  = self._Token
        Headers['Accept']       = client._JSONMimeType

        # Submit request...
        Response = self._submitRequest('/status', 'GET', Headers)

        # Parse response...
        return Response.json()

    # Retrieve songs by their reference...
    def getSongsByReference(self):
        pass

    # Download a song by ID...
    def getSongDownloadById(self):
        pass

    # Download a song by reference...
    def getSongDownloadByReference(self):
        pass

    # Get the URL to the root of all API endpoints...
    def _getURL(self, Endpoint):

        # Remove leading and trailing forward slashes from endpoint...
        Endpoint = Endpoint.rstrip('/')
        Endpoint = Endpoint.lstrip('/')

        # Construct API URL...
        return 'http://{:s}:{:d}/{:s}/{:s}/'.format(self._Host, self._Port, self._Version, Endpoint)

    # Modify a song in the catalogue by its ID...
    def modifySongByID(self):
        pass

    # Modify a song in the catalogue by reference...
    def modifySongByReference(self):
        pass

