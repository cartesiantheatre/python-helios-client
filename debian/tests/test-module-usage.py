#!/usr/bin/env -S python3 -Werror -Wignore::ResourceWarning
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# System imports...
import base64
import glob
import sys
from pprint import pprint
import socket

# Third party imports...
import attr
import helios
from helios.responses import StoredSongSchema

# Entry point...
if __name__ == '__main__':

    # Alert user of what we're doing...
    print('Detecting local IP address...')

    # Allocate a temporary connectionless socket...
    temporary_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Try to establish a "connection"...
    try:
        temporary_socket.connect(('10.255.255.255', 1))
        local_ip_address = temporary_socket.getsockname()[0]

    # If it failed, use loopback address...
    except:
        local_ip_address = '127.0.0.1'

    # Close socket...
    finally:
        temporary_socket.close()

    # Alert user of what we're doing...
    print(F'Local IP address is... {local_ip_address}')

    # Create a client...
    client = helios.Client(host=local_ip_address)

    # Query status...
    print('Querying Helios system status...')
    system_status = client.get_system_status()

    # Show status...
    pprint(attr.asdict(system_status))

    # Unique field for each song reference...
    song_index = 0

    # Add a bunch of songs...
    for song_path in glob.glob("/usr/share/games/lincity-ng/music/default/*.ogg"):

        # Generate unique song index for reference...
        song_index += 1

        # Prepare new song data...
        print(F'Adding song to catalogue... {song_path}')
        new_song_dict = {
            'file': base64.b64encode(open(song_path, 'rb').read()).decode('ascii'),
            'reference': F'some_reference_{song_index}',
            'title': F'some_title_{song_index}'
        }

        # Add the song...
        stored_song = client.add_song(
            new_song_dict=new_song_dict,
            store=True)

        # Prepare to instruct server to delete it's stored copy and change title...
        patch_song_dict = {
            'file' : '',
            'title' : F'patched_title_{stored_song.id}'
        }

        # Patch it...
        print(F'Patching song... {song_path}')
        client.modify_song(
            patch_song_dict=patch_song_dict,
            song_id=stored_song.id)

    # Try to retrieve a random assortment of three songs...
    print('Retrieving random selection of songs...')
    random_songs_list = client.get_random_songs(size=3)

    # Create a schema to serialize stored song objects into JSON...
    stored_song_schema = StoredSongSchema()

    # Show each randomly selected song...
    for random_song in random_songs_list:

        # Show what we retrieved...
        print('Randomly selected record...')
        pprint(stored_song_schema.dump(random_song))

    # Try to get a batch of songs for current page...
    print('Retrieving all songs in catalogue...')
    page_songs_list = client.get_all_songs()

    # Add a learning example...
    client.add_learning_example(
        anchor_song_reference='some_reference_1',
        positive_song_reference='some_reference_2',
        negative_song_reference='some_reference_3')

    # Check to make sure learning example was stored...
    learning_examples = client.get_learning_examples()
    assert(len(learning_examples) == 1)

    # Delete each added song...
    for song in page_songs_list:

        # Show what we're going to delete...
        print('Deleting the following record...')
        pprint(stored_song_schema.dump(song))

        # Delete the record...
        client.delete_song(song_id=song.id)
        print('')

    # Check to make deleting all the songs deleted the learning example too...
    learning_examples = client.get_learning_examples()
    assert(len(learning_examples) == 0)

    # Generate some example triplets...
    learning_examples_list = client.perform_triplet_mining(
        'SEARCH_REFERENCE',
        [
            'SONG_1',
            'SONG_2',
            'SONG_3',
            'SONG_4',
            'SONG_5'
        ],
        [
            'SONG_2',
            'SONG_1',
            'SONG_4'
        ])
    assert(learning_examples_list == 
    [
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_2", negative="SONG_1"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_2", negative="SONG_4"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_2", negative="SONG_3"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_2", negative="SONG_5"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_1", negative="SONG_4"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_1", negative="SONG_3"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_1", negative="SONG_5"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_4", negative="SONG_3"),
        helios.requests.LearningExample(anchor="SEARCH_REFERENCE", positive="SONG_4", negative="SONG_5")
    ])

    # Done...
    print('Done...')
    sys.exit(0)
