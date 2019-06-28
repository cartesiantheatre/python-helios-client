#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
import os
import sys
import requests
import marshmallow
import logging
import json
from http.client import HTTPConnection
from urllib3.exceptions import NewConnectionError, MaxRetryError, ConnectTimeoutError
import helios
from tqdm import tqdm

# i18n...
import gettext
_ = gettext.gettext

# Class to handle all client communication with a Helios server...
class client(object):

    # Class attribute for JSON MIME type...
    _json_mime_type  = 'application/json'

    # Constructor...
    def __init__(self, host, port=6440, token=None, verbose=False, version='v1'):

        # Initialize...
        self._token     = token
        self._host      = host
        self._port      = port
        self._verbose   = verbose
        self._version   = version

        # Initialize headers common to all queries...
        self._common_headers                = {}
        self._common_headers['X-API-Token'] = self._token
        self._common_headers['User-Agent']  = F'helios-python {get_version()}'

        # If verbosity is enabled, toggle in requests and http client libraries...
#        if self._verbose:
#            HTTPConnection.debuglevel = 1
#            logging.basicConfig()
#            logging.getLogger().setLevel(logging.DEBUG)
#            requests_log = logging.getLogger("urllib3")
#            requests_log.setLevel(logging.DEBUG)
#            requests_log.propagate = True

    # Add a new song to your music catalogue...
    def add_song(self, new_song_dict, store=True):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = client._json_mime_type
        headers['Content-Type']     = client._json_mime_type

        # Prepare request...
        query_parameters            = {}
        query_parameters['store']   = str(store).lower()

        # Validate new_song_dict against schema...
        try:
            new_song_schema = helios.requests.NewSongSchema()
            new_song_schema.load(new_song_dict)
        except marshmallow.ValidationError as validationException:
            raise helios.exceptions.Validation(validationException)

        # Submit request and retrieve JSON body...
        response = self._submit_json_request(
            '/songs',
            'POST',
            headers,
            query_parameters,
            new_song_dict)
        stored_song_response_dict = response.json()

        # Extract and construct stored song from response...
        try:
            stored_song_response_schema = helios.responses.StoredSongResponseSchema()
            stored_song_response = stored_song_response_schema.load(stored_song_response_dict)

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as someException:
            raise helios.exceptions.UnexpectedResponse(someException.messages)

        # Parse response...
        return stored_song_response

    # Delete a song by ID or reference...
    def delete_song(self, song_id=None, song_reference=None):

        # Initialize headers...
        headers = self._common_headers

        # Format endpoint...
        if song_id:
            endpoint = F'/songs/by_id/{song_id}'
        elif song_reference:
            endpoint = F'/songs/by_reference/{song_reference}'
        else:
            raise Exception(_('You must provide either a song_id or a song_reference.'))

        # Submit request and retrieve JSON body...
        response = self._submit_json_request(
            endpoint,
            'DELETE',
            headers)

    # Retrieve a list of all songs...
    def get_all_songs(self, page=1, page_size=100):

        # Initialize headers...
        headers                         = self._common_headers
        headers['Accept']               = client._json_mime_type

        # Prepare request...
        query_parameters                = {}
        query_parameters['page']        = int(page)
        query_parameters['page_size']   = int(page_size)

        # Submit request and retrieve JSON body...
        response = self._submit_json_request(
            '/songs/all',
            'GET',
            headers,
            query_parameters)

        # Extract and construct each stored song and add to list...
        try:

            # Storage for list of stored songs...
            stored_song_schema = helios.responses.StoredSongResponseSchema(many=True)
            all_songs_list = stored_song_schema.load(response.json())

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as someException:
            raise helios.exceptions.UnexpectedResponse(someException.messages)

        # Return list of stored songs...
        return all_songs_list

    # Get the complete URL to the endpoint with the  of all API endpoints...
    def _get_endpoint_url(self, endpoint):

        # Remove leading and trailing forward slashes from endpoint...
        endpoint = endpoint.rstrip('/')
        endpoint = endpoint.lstrip('/')

        # Construct API URL...
        url = f'http://{self._host}:{self._port}/{self._version}/{endpoint}/'

        # Show verbosity hint...
        if self._verbose:
            print(_(f'Using endpoint: {url}'))

        # Return constructed URL to caller...
        return url

    # Get server information status...
    def get_server_status(self):

        # Initialize headers...
        headers                 = self._common_headers
        headers['Accept']       = client._json_mime_type

        # Submit request...
        response = self._submit_json_request('/status', 'GET', headers)
        response_dict = response.json()

        # Extract and construct server status...
        try:
            server_status_schema = helios.responses.ServerStatusResponseSchema()
            server_status = server_status_schema.load(response_dict['server_status'])

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as someException:
            raise helios.exceptions.UnexpectedResponse(someException.messages)

        # Parse response...
        return server_status

    # Retrieve the stored song model metadata of a song...
    def get_song(self, song_id=None, song_reference=None):

        # Get the complete URL...
        if song_id:
            endpoint = F'/songs/by_id/{song_id}'
        elif song_reference:
            endpoint = F'/songs/by_reference/{song_reference}'

        # Initialize headers...
        headers                         = self._common_headers
        headers['Accept']               = client._json_mime_type

        # Submit request and retrieve JSON body...
        response = self._submit_json_request(endpoint, 'GET', headers)

        # Extract and construct each stored song and add to list...
        try:

            # Storage for list of single stored songs...
            stored_song_schema = helios.responses.StoredSongResponseSchema(many=True)
            songs_list = stored_song_schema.load(response.json())

            # There should have been only one song retrieved...
            if len(songs_list) is not 1:
                raise helios.exceptions.UnexpectedResponse(
                    _('Expected a single song response.'))

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as someException:
            raise helios.exceptions.UnexpectedResponse(someException.messages)

        # Return single stored song model...
        return songs_list[0]

    # Download a song by ID or reference...
    def get_song_download(self, song_id, song_reference, output, progress=False):

        # Get the complete URL...
        if song_id:
            url = self._get_endpoint_url(F'/songs/download/by_id/{song_id}')
        elif song_reference:
            url = self._get_endpoint_url(F'/songs/download/by_reference/{song_reference}')

        # Initialize headers...
        headers             = self._common_headers
        headers['Accept']   = 'application/octet-stream'

        # Try to download...
        try:

            # Make request to server...
            response = requests.get(url, headers=headers, stream=True)

            # Get total size of response body...
            total_size = int(response.headers.get('content-length'))

            # We reached the server. If we didn't get an expected response,
            #  raise an exception...
            response.raise_for_status()

            # Show progress if requested...
            if progress:
                progress_bar = tqdm(total=total_size, unit=_('bytes'), unit_scale=True)

            # Write out the file...
            with open(output, 'wb') as file:

                # As each chunk streams into memory, write it out...
                for chunk in response.iter_content(chunk_size=8192):

                    # But skip keep-alive chunks...
                    if not chunk:
                        continue

                    # Append chunk to file...
                    file.write(chunk)

                    # Advance progress, if requested...
                    if progress:
                        progress_bar.update(len(chunk))

            # Deallocate progress bar if we created one...
            if progress:
                progress_bar.close()

        # Connection problem...
        except requests.exceptions.ConnectionError as someException:
            raise helios.exceptions.Connection(
                _(f'Unable to connect to {self._host}:{self._port}'))

        # Server reported an error, raise appropriate exception...
        except requests.HTTPError as ServerError:
            self._raise_http_exception(ServerError.response.json())

    # Modify a song in the catalogue...
    def modify_song(self, patch_song_dict, store=None, song_id=None, song_reference=None):

        # Initialize headers...
        headers                 = self._common_headers
        headers['Accept']       = client._json_mime_type
        headers['Content-Type'] = client._json_mime_type

        # Prepare endpoint...
        if song_id is not None:
            endpoint = F'/songs/by_id/{song_id}'
        elif song_reference is not None:
            endpoint = F'/songs/by_reference/{song_reference}'
        else:
            raise helios.exceptions.ExceptionBase(_('You must provide either a song_id or a song_reference.'))

        # Prepare query parameters...
        query_parameters                = {}
        if store is not None:
            query_parameters['store']   = str(store).lower()

        # Validate patch_song_dict against schema...
        try:
            patch_song_schema = helios.requests.PatchSongSchema()
            patch_song_schema.load(patch_song_dict)
        except marshmallow.ValidationError as validationException:
            raise helios.exceptions.Validation(validationException)

        # Submit request and retrieve JSON body...
        response = self._submit_json_request(
            endpoint,
            'PATCH',
            headers,
            query_parameters,
            patch_song_dict)
        response_dict = response.json()

        # Extract and construct server status...
        try:
            stored_song_response_schema = helios.responses.StoredSongResponseSchema()
            stored_song_response = stored_song_response_schema.load(response_dict)

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as someException:
            raise helios.exceptions.UnexpectedResponse(someException.messages)

        # Parse response...
        return stored_song_response

    # Take a server's error response that it emitted as JSON and raise an
    #  appropriate client exception...
    def _raise_http_exception(self, json_response):

        # Extract HTTP code from JSON response...
        code = int(json_response['code'])

        # Extract error details from JSON response...
        details = json_response['details']

        # Extract error summary from JSON response...
        summary = json_response['summary']

        # Bad request exception. Suitable on a 400...
        if code == 400:
            raise helios.exceptions.BadRequest(code, details, summary)

        # Unauthorized exception. Suitable on a 401...
        elif code == 401:
            raise helios.exceptions.Unauthorized(code, details, summary)

        # Not found exception. Suitable on a 404...
        elif code == 404:
            raise helios.exceptions.NotFound(code, details, summary)

        # Internal server error exception. Suitable on a 500...
        elif code == 500:
            raise helios.exceptions.InternalServer(code, details, summary)

        # Insufficient storage exception. Suitable on a 507...
        elif code == 507:
            raise helios.exceptions.InsufficientStorage(code, details, summary)

        # Some other code...
        else:
            raise helios.exceptions.ResponseExceptionBase(code, details, summary)

    # Send a request to endpoint using method, headers, query parameters, and
    #  body...
    def _submit_json_request(self, endpoint, method, headers=dict(), query_parameters=dict(), body=dict()):

        # Get the base URL...
        url = self._get_endpoint_url(endpoint)

        # Try to submit request to server using appropriate HTTP verb...
        try:

            # Perform DELETE request if requested...
            if method == 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    params=query_parameters,
                    json=body)

            # Perform GET request if requested...
            elif method == 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    params=query_parameters,
                    json=body)

            # Perform PATCH request if requested...
            elif method == 'PATCH':
                response = requests.patch(
                    url,
                    headers=headers,
                    params=query_parameters,
                    json=body)

            # Perform POST request if requested...
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    params=query_parameters,
                    json=body)

            # Unknown method...
            else:
                raise Exception(F'Unknown method: {method}')

            # We reached the server. If we didn't get an expected response,
            #  raise an exception...
            response.raise_for_status()

        # Connection problem...
        except requests.exceptions.ConnectionError as someException:
            raise helios.exceptions.Connection(
                _(f'Unable to connect to {self._host}:{self._port}'))

        # Server reported an error, raise appropriate exception...
        except requests.HTTPError as ServerError:
            self._raise_http_exception(ServerError.response.json())

        # Return the response object...
        return response


# Get client version...
def get_version():
    return '0.1'

