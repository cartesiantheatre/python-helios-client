#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# Other imports...
import json
import marshmallow
import os
import simplejson
from tqdm import tqdm
import urllib3
import re
import requests
from requests.adapters import HTTPAdapter, Retry
from requests_toolbelt.utils import user_agent as ua
import shutil
import tempfile
import helios
from helios import __version__
from helios.chunked_upload import chunked_upload
import time

# i18n...
import gettext
_ = gettext.gettext

# Class to handle all client communication with a Helios server...
class Client:

    # Class attribute for JSON MIME type...
    _json_mime_type     = 'application/json'

    # Class attribute for compressed encoding...
    #_accept_encoding    = 'br, gzip, deflate'
    _accept_encoding    = 'gzip'

    # Constructor...
    def __init__(self, host, port=6440, api_key=None, timeout_connect=None, timeout_read=None, tls=True, tls_ca_file=None, tls_certificate=None, tls_key=None, verbose=False, version='v1'):

        # Set default connection timeout if none provided by user...
        if timeout_connect is None:
            timeout_connect = 15

        # Set default read timeout if none provided by user...
        if timeout_read is None:
            timeout_read = 300

        # Initialize...
        self._session           = requests.Session()
        self._host              = host
        self._port              = port
        self._api_key           = api_key
        self._timeout_connect   = timeout_connect
        self._timeout_read      = timeout_read
        self._tls               = tls
        self._tls_ca_file       = tls_ca_file
        self._tls_certificate   = tls_certificate
        self._tls_key           = tls_key
        self._verbose           = verbose
        self._version           = version

        # Prepare a Retry object that will tell our HTTP adapter to retry a
        #  total number of three times and wait one second in between...
        retries = Retry(total=3, backoff_factor=1.0)

        # Construct an adaptor to automatically make three retry attempts on
        #  failed DNS lookups and connection timeouts...
        self._adapter = HTTPAdapter(max_retries=retries)
        self._session.mount('http://', self._adapter)
        self._session.mount('https://', self._adapter)

        # Make sure host provided...
        if host is None:
            raise Exception(_('No host provided.'))

        # Make sure port provided...
        if port is None:
            raise Exception(_('No port provided.'))

        # Configure a user agent builder...
        user_agent = ua.UserAgentBuilder(
            name='helios-python',
            version=get_version())
        user_agent.include_system()

        # Build a user agent string from the builder...
        user_agent_string = user_agent.build()

        # Initialize headers common to all queries...
        self._common_headers                    = {}
        self._common_headers['Accept-Encoding'] = 'identity'
        self._common_headers['User-Agent']      = user_agent_string

        # If an API key was provided by user, add it to request headers...
        if api_key is not None:
            self._common_headers['X-API-Key']   = self._api_key

        # If verbosity is enabled, toggle in requests and http client libraries...
#        if self._verbose:
#            HTTPConnection.debuglevel = 1
#            logging.basicConfig()
#            logging.getLogger().setLevel(logging.DEBUG)
#            requests_log = logging.getLogger("urllib3")
#            requests_log.setLevel(logging.DEBUG)
#            requests_log.propagate = True

    # Add the given learning example triplet...
    def add_learning_example(self, anchor_song_reference, positive_song_reference, negative_song_reference):

        # Construct a list of the caller's single triplet...
        single_triplet_list = [(anchor_song_reference, positive_song_reference, negative_song_reference)]

        # Upload to server...
        self.add_learning_examples(single_triplet_list)

    # Add the given list of learning example triplets...
    def add_learning_examples(self, learning_example_triplets):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Content-Type']     = Client._json_mime_type

        # Construct list of learning example objects from triplet list...
        learning_examples = [
            helios.requests.LearningExample(anchor, positive, negative) for
            (anchor, positive, negative) in learning_example_triplets
        ]

        # Construct learning example schema to transform learning example list
        #  into JSON...
        learning_example_schema = helios.requests.LearningExampleSchema(many=True)

        # Submit request...
        response = self._submit_request(
            endpoint='/learning/examples',
            method='POST',
            headers=headers,
            data=learning_example_schema.dumps(learning_examples))

    # Add a new song to your music catalogue, optionally store it after
    #  analysis, and optionally invoke a progress callback of the from
    #  foo(bytes_read, new_bytes, total_bytes)...
    def add_song(self, new_song_dict, store=True, progress_callback=None):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Accept-Encoding']  = Client._accept_encoding
        headers['Content-Type']     = Client._json_mime_type

        # Prepare request...
        query_parameters            = {}
        query_parameters['store']   = str(store).lower()

        # Validate new_song_dict against schema...
        try:
            new_song_schema = helios.requests.NewSongSchema()
            new_song_schema.load(new_song_dict)
        except marshmallow.ValidationError as some_exception:
            raise helios.exceptions.Validation(some_exception) from some_exception

        # Submit request...
        response = self._submit_request(
            endpoint='/songs',
            method='POST',
            headers=headers,
            query_parameters=query_parameters,
            data=chunked_upload(
                data=bytes(json.dumps(new_song_dict), encoding='utf-8'),
                progress_callback=progress_callback))

        # Extract and construct stored song from response...
        try:
            stored_song_response_schema = helios.responses.StoredSongSchema()
            stored_song_response = stored_song_response_schema.load(response.json())

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Parse response...
        return stored_song_response

    # Delete all learning examples...
    def delete_all_learning_examples(self):

        # Initialize headers...
        headers = self._common_headers

        # Submit request...
        self._submit_request(
            endpoint='/learning/examples/all',
            method='DELETE',
            headers=headers)

    # Delete a learning example...
    def delete_learning_example(self, anchor_song_reference, positive_song_reference, negative_song_reference):

        # Initialize headers...
        headers                         = self._common_headers

        # Prepare request...
        query_parameters                = {}
        query_parameters['anchor']      = anchor_song_reference
        query_parameters['positive']    = positive_song_reference
        query_parameters['negative']    = negative_song_reference

        # Submit request...
        response = self._submit_request(
            endpoint='/learning/examples',
            method='DELETE',
            headers=headers,
            query_parameters=query_parameters)

    # Delete an asynchronous job running on the server by job ID...
    def delete_job(self, job_id):

        # Initialize headers...
        headers = self._common_headers

        # Format endpoint...
        endpoint = F'/status/jobs/{job_id}'

        # Submit request...
        self._submit_request(
            endpoint=endpoint,
            method='DELETE',
            headers=headers)

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

        # Submit request...
        self._submit_request(
            endpoint=endpoint,
            method='DELETE',
            headers=headers)

    # Retrieve a list of all songs...
    def get_all_songs(self, page=None, page_size=None, progress=False, save_catalogue=None):

        # 3m32.299s with pagination for entire catalogue

        # Initialize headers...
        headers                             = self._common_headers
        headers['Accept']                   = Client._json_mime_type
        headers['Accept-Encoding']          = Client._accept_encoding

        # Endpoint to retrieve all songs...
        url = self._get_endpoint_url('/songs/all')

        # Storage for query parameters...
        query_parameters                    = {}

        # Create a temp file for the decompressed version...
        [tempfile_fd, tempfile_name] = tempfile.mkstemp(
            prefix="helios_client_get_all_songs_")

        # If user requested pagination, format endpoint URL with that as query
        #  parameters...
        if page is not None and page_size is not None:
            url = self._get_endpoint_url(F'/songs/all?page={int(page)}&page_size={int(page_size)}')

        # Flag to requests on whether to verify server certificate. This can be
        #  either a boolean or a string according to documentation...
        verify = False

        # Tuple to public and private keys, if set...
        public_private_key = None

        # TLS was requested, so prepare to use associated settings...
        if self._tls:

            # If no certificate authority was provided, disable server
            #  certificate verification...
            if not self._tls_ca_file:
                verify = False
                urllib3.disable_warnings()

            # Otherwise set to path to certificate authority file...
            else:
                verify = self._tls_ca_file

            # Set certificate public and private key, if provided...
            if self._tls_certificate or self._tls_key:
                public_private_key = (self._tls_certificate, self._tls_key)

        # Submit request, extract, construct each stored song and add to list...
        try:

            # Submit request...
            response = self._session.get(
                url=url,
                headers=headers,
                stream=True,
                verify=verify)

            # We reached the server. If we didn't get an expected response,
            #  raise an exception...
            response.raise_for_status()

            # Get total size of response body...
            total_size = int(response.headers.get('content-length'))

            # Show progress if requested...
            if progress:
                progress_bar = tqdm(total=total_size, unit=_('B'), unit_scale=True)

            # As each chunk streams into memory, write it out...
            for chunk in response.iter_content(chunk_size=8192):

                # But skip keep-alive chunks...
                if not chunk:
                    continue

                # Advance progress, if requested...
                if progress:
                    progress_bar.update(len(chunk))

                # Save response to temp file...
                os.write(tempfile_fd, chunk)

            # Close temp file...
            os.close(tempfile_fd)

            # Deallocate progress bar if we created one...
            if progress:
                progress_bar.close()

            # Load the JSON from disk...
            json_data = None
            with open(tempfile_name, "r") as file:
                json_data = json.load(file)

            # Validate response...
            stored_song_schema = helios.responses.StoredSongSchema(many=True)
            all_songs_list = stored_song_schema.load(json_data)

            # If user requested to save response to disk, move the temp file
            #  to user's preference...
            if save_catalogue:
                shutil.move(tempfile_name, save_catalogue)

        # Check if songs to retrieve...
        except requests.HTTPError as some_exception:

            # No songs available. Return empty list...
            if some_exception.response.status_code == 404:
                return []

            # Otherwise some other HTTP error...
            else:
                self._raise_http_exception(some_exception.response.json())

        # No more songs...
        except requests.exceptions.InvalidURL:
            return []

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Return list of stored songs...
        return all_songs_list

    # Get the complete URL to the endpoint with the  of all API endpoints...
    def _get_endpoint_url(self, endpoint):

        # Remove leading and trailing forward slashes from endpoint...
        endpoint = endpoint.rstrip('/')
        endpoint = endpoint.lstrip('/')

        # Construct protocol portion of API url...
        if self._tls:
            url = 'https://'
        else:
            url = 'http://'

        # Construct rest of URL to endpoint...
        url += f'{self._host}:{self._port}/{self._version}/{endpoint}'

        # Show verbosity hint...
        #if self._verbose:
        #    print(_(f'Using endpoint: {url}'))

        # Return constructed URL to caller...
        return url

    # Get system status about server...
    def get_system_status(self):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Accept-Encoding']  = Client._accept_encoding

        # Submit request...
        response = self._submit_request(
            endpoint='/status/system',
            method='GET',
            headers=headers)

        # Extract and construct system status...
        try:
            response_dict = response.json()
            system_status_schema = helios.responses.SystemStatusSchema()
            system_status = system_status_schema.load(response_dict['system_status'])

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Parse response...
        return system_status

    # Get information about available genres on the server...
    def get_genres_information(self):

        # Initialize headers...
        headers                 = self._common_headers
        headers['Accept']       = Client._json_mime_type

        # Submit request, extract, construct each genre information and add to
        #  list...
        try:

            # Submit request...
            response = self._submit_request(
                endpoint='/songs/genres',
                method='GET',
                headers=headers)

            # Validate response...
            genre_information_schema = helios.responses.GenreInformationSchema(many=True)
            genre_information_list = genre_information_schema.load(response.json())

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Return list of genres and information about each...
        return genre_information_list

    # Get job status from server, returning the HTTP status code and the
    #  object the server sent us...
    def get_job_status(self, job_id, schema):

        # Initialize headers...
        headers                 = self._common_headers
        headers['Accept']       = Client._json_mime_type

        # Format endpoint...
        endpoint = F'/status/jobs/{job_id}'

        # Submit request...
        response = self._submit_request(
            endpoint=endpoint,
            method='GET',
            headers=headers)

        # Extract and deserialize response...
        try:

            # Convert the incoming JSON into a dictionary...
            response_dict = response.json()

            # Final result ready...
            if response.status_code == 200:

                # Storage for list of stored songs...
                response_object = schema.load(response.json())

                # Return status code and deserialized object to caller...
                return (response.status_code, response_object)

            # Status update ready...
            elif response.status_code == 202:

                # Storage for job status...
                job_status_schema = helios.responses.JobStatusSchema()
                job_status = job_status_schema.load(response_dict)

                # Return status code and deserialized object to caller...
                return (response.status_code, job_status)

            # Server reported an error. Raise an exception...
            elif response.status_code >= 400:
                self._raise_http_exception(response_dict)

            # For all other responses treat it as though it was unexpected...
            else:
                raise helios.exceptions.UnexpectedResponse(
                    _(F'Unexpected server response while polling job status: {response.status_code}'))

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

    # Retrieve a list of all learning examples...
    def get_learning_examples(self):

        # Initialize headers...
        headers                         = self._common_headers
        headers['Accept']               = Client._json_mime_type
        headers['Accept-Encoding']      = Client._accept_encoding

        # Submit request, extract, construct each learning example and add to
        #  list...
        try:

            # Submit request...
            response = self._submit_request(
                endpoint='/learning/examples/all',
                method='GET',
                headers=headers)

            # Validate response...
            learning_example_schema = helios.responses.LearningExampleSchema(many=True)
            all_learning_examples = learning_example_schema.load(response.json())

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Return list of learning examples...
        return all_learning_examples

    # Get a single random song...
    def get_random_song(self):

        # Retrieve the list of a single song...
        random_songs_list = self.get_random_songs(size=1)

        # Return it...
        return random_songs_list[0]

    # Retrieve a list of random songs...
    def get_random_songs(self, size=1):

        # Initialize headers...
        headers                         = self._common_headers
        headers['Accept']               = Client._json_mime_type
        headers['Accept-Encoding']      = Client._accept_encoding

        # Prepare request...
        query_parameters                = {}
        query_parameters['size']        = int(size)

        # Submit request, extract, construct each stored song and add to list...
        try:

            # Submit request...
            response = self._submit_request(
                endpoint='/songs/random',
                method='GET',
                headers=headers,
                query_parameters=query_parameters)

            # Validate response...
            stored_song_schema = helios.responses.StoredSongSchema(many=True)
            random_songs_list = stored_song_schema.load(response.json())

        # No more songs...
        except helios.exceptions.NotFound:
            return []

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Return list of stored songs...
        return random_songs_list

    # Perform a similarity search within the music catalogue...
    def get_similar_songs(self, similarity_search_dict, progress=False):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Content-Type']     = Client._json_mime_type
        headers['Accept-Encoding']  = Client._accept_encoding
        headers['X-Helios-Expect']  = '202-accepted'

        # Validate similarity_search_dict against schema...
        try:
            similarity_search_schema = helios.requests.SimilaritySearchSchema()
            similarity_search_schema.load(similarity_search_dict)
        except marshmallow.ValidationError as some_exception:
            raise helios.exceptions.Validation(some_exception) from some_exception

        # Submit request...
        response = self._submit_request(
            endpoint='/songs/similar',
            method='POST',
            headers=headers,
            data=json.dumps(similarity_search_dict))

        # Verify server sent Location response header...
        if 'Location' not in response.headers:
            raise helios.exceptions.UnexpectedResponse(
                _('Location header missing from server response.'))

        # Parse Location header for job ID which points to where job status can
        #  be tracked...
        location = response.headers.get('Location')
        location_regex = re.compile(FR"^/{self._version}/status/jobs/(\d+)$")
        matches = re.fullmatch(location_regex, location)

        # Check to ensure job ID could be parsed...
        if not matches:
            raise helios.exceptions.UnexpectedResponse(
                _(F'Location header malformed: {location}'))

        # Extract job ID...
        job_id = matches.group(1)

        # Log job ID...
        if self._verbose:
            print(_(F'Server reported job started with job ID {job_id}...'))

        # Optional progress bar, if requested by user and we have enough
        #  information to manage one...
        progress_bar = None

        # Try to monitor progress until final update is available...
        try:

            # Status code received from server each time we poll it...
            status_code = 0

            # Counter of the number of bytes the server has fetched...
            bytes_fetched = 0

            # Keep polling until final update is received...
            while True:

                # Wait a second after each query...
                time.sleep(1.0)

                # Query server for response code and object...
                status_code, response_object = self.get_job_status(
                    job_id,
                    helios.responses.StoredSongSchema(many=True))

                # Result is ready...
                if status_code == 200:

                    # Get the songs' list...
                    songs_list = response_object

                    # Return list to user...
                    return songs_list

                # Status update available, but final result not ready yet...
                if status_code == 202:

                    # Get the job's status...
                    job_status = response_object

                    # If a progress bar was requested and does not exist yet,
                    #  construct it...
                    if progress and progress_bar is None and job_status.progress_total is not None:
                        progress_bar = tqdm(total=job_status.progress_total, unit='B', unit_scale=True)

                    # If a progress bar exists, update it...
                    if progress_bar is not None:

                        # Update progress bar...
                        progress_bar.update(job_status.progress_current - bytes_fetched)

                        # Track the number of bytes server fetched for next
                        #  iteration...
                        bytes_fetched = job_status.progress_current

                        # Set description...
                        progress_bar.set_description(job_status.message)

                # For all other responses treat it as though it was unexpected...
                else:
                    raise helios.exceptions.UnexpectedResponse(
                        _(F'Unexpected server response while polling job status: {response.status_code}'))

        # User trying to abort...
        except KeyboardInterrupt as someException:

            # Notify user we heard them...
            print(_(F'\rAborting. Please wait a moment...'))

            # Ask server to delete the job...
            self.delete_job(job_id)

            # Propagate interrupt up the chain...
            raise someException

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Cleanup tasks...
        finally:

            # Deallocate progress bar if we created one...
            if progress_bar is not None:
                progress_bar.close()

    # Retrieve the stored song model metadata of a song...
    def get_song(self, song_id=None, song_reference=None):

        # Get the complete URL...
        if song_id:
            endpoint = F'/songs/by_id/{song_id}'
        elif song_reference:
            endpoint = F'/songs/by_reference/{song_reference}'
        else:
            raise helios.exceptions.ExceptionBase(_('You must provide either a song_id or a song_reference.'))

        # Initialize headers...
        headers                         = self._common_headers
        headers['Accept']               = Client._json_mime_type
        headers['Accept-Encoding']      = Client._accept_encoding

        # Submit request...
        response = self._submit_request(
            endpoint=endpoint,
            method='GET',
            headers=headers)

        # Extract and construct each stored song and add to list...
        try:
            stored_song_schema = helios.responses.StoredSongSchema(many=True)
            songs_list = stored_song_schema.load(response.json())

            # There should have been only one song retrieved...
            if len(songs_list) != 1:
                raise helios.exceptions.UnexpectedResponse(
                    _('Expected a single song response.'))

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Return single stored song model...
        return songs_list[0]

    # Retrieve the artwork for the given song as a tupel of a byte array and
    #  MIME type...
    def get_song_artwork(self, song_id=None, song_reference=None, maximum_height=None, maximum_width=None):

        # Get the complete URL...
        if song_id:
            endpoint = F'/songs/download_artwork/by_id/{song_id}'
        elif song_reference:
            endpoint = F'/songs/download_artwork/by_reference/{song_reference}'
        else:
            raise helios.exceptions.ExceptionBase(_('You must provide either a song_id or a song_reference.'))

        # Initialize headers...
        headers = self._common_headers

        # Prepare query parameters...
        query_parameters                        = {}
        if maximum_height:
            query_parameters['maximum_height']  = int(maximum_height)
        if maximum_width:
            query_parameters['maximum_width']   = int(maximum_width)

        # Submit request...
        response = self._submit_request(
            endpoint=endpoint,
            method='GET',
            headers=headers,
            query_parameters=query_parameters)

        # Return binary data array and MIME type...
        return response.content, response.headers.get('Content-Type')

    # Download a song by ID or reference...
    def get_song_download(self, output, song_id=None, song_reference=None, tui_progress=False, progress_callback=None):

        # Get the complete URL...
        if song_id:
            url = self._get_endpoint_url(F'/songs/download/by_id/{song_id}')
        elif song_reference:
            url = self._get_endpoint_url(F'/songs/download/by_reference/{song_reference}')
        else:
            raise Exception(_('You must provide either a song_id or a song_reference when calling get_song_download.'))

        # Initialize headers...
        headers             = self._common_headers
        headers['Accept']   = 'application/octet-stream'

        # Flag to requests on whether to verify server certificate. This can be
        #  either a boolean or a string according to documentation...
        verify = False

        # Tuple to public and private keys, if set...
        public_private_key = None

        # TLS was requested, so prepare to use associated settings...
        if self._tls:

            # If no certificate authority was provided, disable server
            #  certificate verification...
            if not self._tls_ca_file:
                verify = False
                urllib3.disable_warnings()

            # Otherwise set to path to certificate authority file...
            else:
                verify = self._tls_ca_file

            # Set certificate public and private key, if provided...
            if self._tls_certificate or self._tls_key:
                public_private_key = (self._tls_certificate, self._tls_key)

        # Try to download...
        try:

            # Make request to server...
            response = self._session.get(
                url,
                headers=headers,
                stream=True,
                verify=verify,
                cert=public_private_key)

            # We reached the server. If we didn't get an expected response,
            #  raise an exception...
            response.raise_for_status()

            # Get total size of response body...
            total_size = int(response.headers.get('content-length'))

            # Total size of downloaded data...
            current_size = 0

            # Show TUI progress if requested...
            if tui_progress:
                tui_progress_bar = tqdm(total=total_size, unit=_('B'), unit_scale=True)

            # Write out the file...
            with open(output, 'wb') as file:

                # As each chunk streams into memory, write it out...
                for chunk in response.iter_content(chunk_size=8192):

                    # But skip keep-alive chunks...
                    if not chunk:
                        continue

                    # Append chunk to file...
                    file.write(chunk)

                    # Get current chunk size...
                    chunk_size = len(chunk)

                    # Add to total downloaded size...
                    current_size += chunk_size

                    # Advance TUI progress, if requested...
                    if tui_progress:
                        tui_progress_bar.update(chunk_size)

                    # If user provided a progress callback, invoke it...
                    if progress_callback:
                        progress_callback(current_size=current_size, total_size=total_size)

            # Deallocate TUI progress bar if we created one...
            if tui_progress:
                tui_progress_bar.close()

        # Connection problem...
        except requests.exceptions.ConnectionError as some_exception:
            raise helios.exceptions.Connection(
                _(f'Unable to connect to {self._host}:{self._port}')) from some_exception

        # Server reported an error, raise appropriate exception...
        except requests.HTTPError as some_exception:
            self._raise_http_exception(some_exception.response.json())

    # Modify a song in the catalogue...
    def modify_song(self, patch_song_dict, store=None, song_id=None, song_reference=None):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Content-Type']     = Client._json_mime_type
        headers['Accept-Encoding']  = Client._accept_encoding

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
        except marshmallow.ValidationError as some_exception:
            raise helios.exceptions.Validation(some_exception) from some_exception

        # Submit request...
        response = self._submit_request(
            endpoint=endpoint,
            method='PATCH',
            headers=headers,
            query_parameters=query_parameters,
            data=json.dumps(patch_song_dict))

        # Extract and construct server response...
        try:
            stored_song_response_schema = helios.responses.StoredSongSchema()
            stored_song_response = stored_song_response_schema.load(response.json())

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Parse response...
        return stored_song_response

    # Perform training on learning examples...
    def perform_training(self, tui_progress=False):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Content-Type']     = Client._json_mime_type
        headers['X-Helios-Expect']  = '202-accepted'

        # Construct perform training object...
        perform_training = helios.requests.PerformTraining()

        # Construct perform training schema to transform request into JSON...
        perform_training_schema = helios.requests.PerformTrainingSchema()

        # Submit request...
        response = self._submit_request(
            endpoint='/learning/perform',
            method='POST',
            headers=headers,
            data=perform_training_schema.dumps(perform_training))

        # Verify server sent Location response header...
        if 'Location' not in response.headers:
            raise helios.exceptions.UnexpectedResponse(
                _('Location header missing from server response.'))

        # Parse Location header for job ID which points to where job status can
        #  be tracked...
        location = response.headers.get('Location')
        location_regex = re.compile(FR"^/{self._version}/status/jobs/(\d+)$")
        matches = re.fullmatch(location_regex, location)

        # Check to ensure job ID could be parsed...
        if not matches:
            raise helios.exceptions.UnexpectedResponse(
                _(F'Location header malformed: {location}'))

        # Extract job ID...
        job_id = matches.group(1)

        # Log job ID...
        if self._verbose:
            print(_(F'Server reported job started with job ID {job_id}...'))

        # Optional TUI progress bar, if requested by user and we have enough
        #  information to manage one...
        tui_progress_bar = None

        # Try to monitor progress until final update is available...
        try:

            # Status code received from server each time we poll it...
            status_code = 0

            # Keep polling until final update is received...
            while True:

                # Wait a second after each query...
                time.sleep(1.0)

                # Query server for response code and object...
                status_code, response_object = self.get_job_status(
                    job_id,
                    helios.responses.TrainingReportSchema())

                # Result is ready...
                if status_code == 200:

                    # Get the training report...
                    training_report = response_object

                    # Return it to user...
                    return training_report

                # Status update available, but final result not ready yet...
                if status_code == 202:

                    # Get the job's status...
                    job_status = response_object

                    # If a TUI progress bar was requested and does not exist
                    #  yet, construct it...
                    if tui_progress and tui_progress_bar is None and job_status.progress_total is not None:
                        tui_progress_bar = tqdm(total=job_status.progress_total)

                    # If a TUI progress bar exists, update it...
                    if tui_progress_bar is not None:

                        # Update progress bar...
                        tui_progress_bar.update(job_status.progress_current)

                        # Set description...
                        tui_progress_bar.set_description(job_status.message)

                # For all other responses treat it as though it was unexpected...
                else:
                    raise helios.exceptions.UnexpectedResponse(
                        _(F'Unexpected server response while polling job status: {response.status_code}'))

        # User trying to abort...
        except KeyboardInterrupt as someException:

            # Notify user we heard them...
            print(_(F'\rAborting. Please wait a moment...'))

            # Ask server to delete the job...
            self.delete_job(job_id)

            # Propagate interrupt up the chain...
            raise someException

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Cleanup tasks...
        finally:

            # Deallocate TUI progress bar if we created one...
            if tui_progress_bar is not None:
                tui_progress_bar.close()

    # Perform triplet mining from the system and user generated rankings for the
    #  given search key and return list of triplets...
    def perform_triplet_mining(self, search_reference, system_rankings, user_rankings):

        # Initialize headers...
        headers                     = self._common_headers
        headers['Accept']           = Client._json_mime_type
        headers['Content-Type']     = Client._json_mime_type
        headers['Accept-Encoding']  = Client._accept_encoding

        # Construct perform triplet mining request object...
        perform_triplet_mining = helios.requests.PerformTripletMining(
            search_reference,
            system_rankings,
            user_rankings)

        # Construct perform triplet mining request schema to transform request
        #  into JSON...
        perform_triplet_mining_schema = helios.requests.PerformTripletMiningSchema()

        # Try to submit request, extract, construct each received triplet and
        #  add to list...
        try:

            # Submit request...
            response = self._submit_request(
                endpoint='/learning/examples/mine',
                method='POST',
                headers=headers,
                data=perform_triplet_mining_schema.dumps(perform_triplet_mining))

            # Validate response...
            learning_examples_schema = helios.responses.LearningExampleSchema(many=True)
            learning_examples_list = learning_examples_schema.load(response.json())

        # Deserialization error...
        except marshmallow.exceptions.MarshmallowError as some_exception:
            raise helios.exceptions.UnexpectedResponse(some_exception) from some_exception

        # Return the server generated list of learning examples...
        return learning_examples_list

    # Take a server's error response that it emitted as JSON and raise an
    #  appropriate client exception...
    def _raise_http_exception(self, json_response):

        # Extract HTTP code from JSON response...
        code = 0
        if 'code' in json_response:
            code = int(json_response['code'])

        # Extract error details from JSON response...
        details = 'A problem occurred, but the server provided no details.'
        if 'details' in json_response:
            details = json_response['details']

        # Extract error summary from JSON response...
        summary = 'Server provided no summary.'
        if 'summary' in json_response:
            summary = json_response['summary']

        # Bad request exception. Suitable on a 400...
        if code == 400:
            raise helios.exceptions.BadRequest(code, details, summary) from None

        # Unauthorized exception. Suitable on a 401...
        elif code == 401:
            raise helios.exceptions.Unauthorized(code, details, summary) from None

        # Not found exception. Suitable on a 404...
        elif code == 404:
            raise helios.exceptions.NotFound(code, details, summary) from None

        # Conflict exception. Suitable on a 409...
        elif code == 409:
            raise helios.exceptions.Conflict(code, details, summary) from None

        # Internal server error exception. Suitable on a 500...
        elif code == 500:
            raise helios.exceptions.InternalServer(code, details, summary) from None

        # Insufficient storage exception. Suitable on a 507...
        elif code == 507:
            raise helios.exceptions.InsufficientStorage(code, details, summary) from None

        # Some other code...
        else:
            raise helios.exceptions.ResponseExceptionBase(code, details, summary) from None

    # Send a request to endpoint using method, headers, query parameters, and
    #  body...
    def _submit_request(
        self,
        endpoint,
        method,
        headers=None,
        query_parameters=None,
        data=bytes()):

        # Request timeout tuple in seconds. First parameter is connect timeout
        #  with the second being the read timeout...
        timeout = (self._timeout_connect, self._timeout_read)

        # Get the base URL...
        url = self._get_endpoint_url(endpoint)

        # Flag to requests on whether to verify server certificate. This can be
        #  either a boolean or a string according to documentation...
        verify = False

        # Tuple to public and private keys, if set...
        public_private_key = None

        # TLS was requested, so prepare to use associated settings...
        if self._tls:

            # If no certificate authority was provided, disable server
            #  certificate verification...
            if not self._tls_ca_file:
                verify = False
                urllib3.disable_warnings()

            # Otherwise set to path to certificate authority file...
            else:
                verify = self._tls_ca_file

            # Set certificate public and private key, if provided...
            if self._tls_certificate or self._tls_key:
                public_private_key = (self._tls_certificate, self._tls_key)

        # Try to submit request to server using appropriate HTTP verb...
        try:

            # Perform DELETE request if requested...
            if method == 'DELETE':
                response = self._session.delete(
                    url,
                    headers=headers,
                    params=query_parameters,
                    data=data,
                    timeout=timeout,
                    verify=verify,
                    cert=public_private_key)

            # Perform GET request if requested...
            elif method == 'GET':
                response = self._session.get(
                    url,
                    headers=headers,
                    params=query_parameters,
                    data=data,
                    timeout=timeout,
                    verify=verify,
                    cert=public_private_key)

            # Perform PATCH request if requested...
            elif method == 'PATCH':
                response = self._session.patch(
                    url,
                    headers=headers,
                    params=query_parameters,
                    data=data,
                    timeout=timeout,
                    verify=verify,
                    cert=public_private_key)

            # Perform POST request if requested...
            elif method == 'POST':
                response = self._session.post(
                    url,
                    headers=headers,
                    params=query_parameters,
                    data=data,
                    timeout=timeout,
                    verify=verify,
                    cert=public_private_key)

            # Unknown method...
            else:
                raise Exception(F'Unknown method: {method}') from None

            # We reached the server. If we didn't get an expected response,
            #  raise an exception...
            response.raise_for_status()

        # Can't establish connection problem...
        except requests.exceptions.ReadTimeout as some_exception:
            raise helios.exceptions.Connection(
                _(F'Read timeout awaiting response from {self._host}:{self._port}')) from some_exception

        # Connection timeout...
        except requests.exceptions.ConnectTimeout as some_exception:
            raise helios.exceptions.Connection(
                _(F'Connection timeout while trying to connect to {self._host}:{self._port}')) from some_exception

        # Some other connection problem...
        except requests.exceptions.ConnectionError as some_exception:
            raise helios.exceptions.Connection(
                _(F'Connection error while connecting to {self._host}:{self._port}')) from some_exception

        # URL not found...
        except requests.exceptions.InvalidURL as some_exception:
            raise helios.exceptions.NotFound(_(F'URL not found at: {url}')) from some_exception

        # Server reported an error, raise appropriate exception...
        except requests.exceptions.HTTPError as some_exception:
            try:
                some_exception.response.json()
            except simplejson.errors.JSONDecodeError:
                raise helios.exceptions.ResponseExceptionBase(
                    code=some_exception.response.status_code,
                    details=F'Server response had no JSON body, but code {some_exception.response.status_code}.',
                    summary=F'Server response had no JSON body, but code {some_exception.response.status_code}.') from some_exception
            self._raise_http_exception(some_exception.response.json())

        # Return the response object...
        return response


# Get client version...
def get_version():
    return __version__.version
