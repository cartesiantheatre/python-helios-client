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
from helios import exceptions
from helios import responses

# i18n...
import gettext
_ = gettext.gettext

# Class to handle all client communication with a Helios server...
class client(object):

    # Class attribute for JSON MIME type...
    _json_mime_type  = 'application/json'

    # Constructor...
    def __init__(self, token, host, port=6440, version='v1'):

        # Initialize...
        self._token     = token
        self._host      = host
        self._port      = port
        self._version   = version

    # Add a new song to your music catalogue...
    def add_song(self, store=True, new_song=dict()):

        # Initialize headers...
        headers = {}
        headers['X-API-Token']  = self._token
        headers['Accept']       = client._json_mime_type
        headers['Content-Type'] = client._json_mime_type

        # Prepare request...
        response = requests.post(
            self._get_url('/songs'),
            params={'store': str(store).lower()},
            headers=headers,
            json=new_song)

        # Check response OK...
        self._submit_request(response, 201)

        # Retrieve JSON body...
        json_response = response.json()

        # Return constructed stored song from response...
        return responses.StoredSongResponse(
            album=json_response['album'],
            algorithm_age=int(json_response['algorithm_age']),
            artist=json_response['artist'],
            duration=int(json_response['duration']),
            genre=json_response['genre'],
            id=int(json_response['id']),
            isrc=json_response['isrc'],
            location=json_response['location'],
            reference=json_response['reference'],
            title=json_response['title'],
            year=int(json_response['year']))

    # Check to ensure an HTTP response was as expected, and if not, to raise an
    #  appropriate exception...
    def _submit_request(self, endpoint, method, headers=dict()):

        # Get the base URL...
        url = self._get_url(endpoint)

        # Try to submit request to server using appropriate HTTP verb...
        try:

            # Perform GET request if requested...
            if method == 'GET':
                response = requests.get(url, headers=headers)

            # We reached the server. If we didn't get an expected response,
            #  raise an exception...
            response.raise_for_status()

        # Server reported an error...
        except requests.HTTPError as ServerError:

            # Try to get the response body...
            json_response = ServerError.response.json()

            # Extract HTTP code from JSON response...
            code = int(json_response['code'])

            # Extract error details from JSON response...
            details = json_response['details']

            # Extract error summary from JSON response...
            summary = json_response['summary']

            # Bad request exception. Suitable on a 400...
            if code == 400:
                raise exceptions.BadRequest(code, details, summary)

            # Unauthorized exception. Suitable on a 401...
            elif code == 401:
                raise exceptions.Unauthorized(code, details, summary)

            # Not found exception. Suitable on a 404...
            elif code == 404:
                raise exceptions.NotFound(code, details, summary)

            # Internal server error exception. Suitable on a 500...
            elif code == 500:
                raise exceptions.InternalServer(code, details, summary)

            # Insufficient storage exception. Suitable on a 507...
            elif code == 507:
                raise exceptions.InsufficientStorage(code, details, summary)

            # Some other code...
            else:
                raise exceptions.HeliosExceptionBase(code, details, summary)

        # Return the response object...
        return response

    # Delete a song or songs by their ID...
    def delete_songs_by_id(self):
        pass

    # Delete songs by their reference...
    def delete_songs_by_reference(self):
        pass

    # Retrieve a list of all songs...
    def get_all_songs(self):
        pass

    # Search for a similar song or songs...
    def get_similar_songs(self):
        pass

    # Retrieve a song or songs by their IDs...
    def get_songs_by_id(self, song_id):
        return requests.get(self._get_url(f'/songs/by_id/{song_id}/', headers={'Accept': 'application/json'}))

    # Get server information status as JSON...
    def get_server_status(self):

        # Initialize headers...
        headers = {}
        headers['X-API-Token']  = self._token
        headers['Accept']       = client._json_mime_type

        # Submit request...
        response = self._submit_request('/status', 'GET', headers=headers)

        # Parse response...
        return response.json()

    # Retrieve songs by their reference...
    def get_songs_by_reference(self):
        pass

    # Download a song by ID...
    def get_song_download_by_id(self):
        pass

    # Download a song by reference...
    def get_song_download_by_reference(self):
        pass

    # Get the URL to the root of all API endpoints...
    def _get_url(self, endpoint):

        # Remove leading and trailing forward slashes from endpoint...
        endpoint = endpoint.rstrip('/')
        endpoint = endpoint.lstrip('/')

        # Construct API URL...
        return f'http://{self._host}:{self._port}/{self._version}/{endpoint}/'

    # Modify a song in the catalogue by its ID...
    def modify_song_by_id(self):
        pass

    # Modify a song in the catalogue by reference...
    def modify_song_by_reference(self):
        pass

