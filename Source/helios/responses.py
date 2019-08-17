#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
import attr
from marshmallow import Schema, fields, post_load

# Stored song response after adding, modifying, or retrieving a song...
@attr.s
class StoredSong:
    album           = attr.ib()
    algorithm_age   = attr.ib()
    artist          = attr.ib()
    duration        = attr.ib()
    genre           = attr.ib()
    id              = attr.ib()
    isrc            = attr.ib()
    location        = attr.ib()
    reference       = attr.ib()
    title           = attr.ib()
    year            = attr.ib()


# Stored song response schema after adding, modifying, or retrieving a song...
class StoredSongSchema(Schema):

    # Fields...
    album           = fields.String(required=True)
    algorithm_age   = fields.Integer(required=True)
    artist          = fields.String(required=True)
    duration        = fields.Integer(required=True)
    genre           = fields.String(required=True)
    id              = fields.Integer(required=True)
    isrc            = fields.String(required=True)
    location        = fields.String(required=True)
    reference       = fields.String(required=True)
    title           = fields.String(required=True)
    year            = fields.Integer(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_stored_song(self, data, **kwargs):
        return StoredSong(**data)


# Server error response...
@attr.s
class Error:
    code    = attr.ib()
    details = attr.ib()
    summary = attr.ib()


# Server error response schema...
class ErrorSchema(Schema):

    # Fields...
    code            = fields.Integer(required=True)
    details         = fields.String(required=True)
    summary         = fields.String(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_error(self, data, **kwargs):
        return Error(**data)


# CPU load status field of server CPU status request response...
@attr.s
class ServerCPULoadStatus:
    all                            = attr.ib()
    individual                     = attr.ib()


# CPU load status field of server CPU status request response schema...
class ServerCPULoadStatusSchema(Schema):

    # Fields...
    all                            = fields.Integer(required=True)
    individual                     = fields.List(fields.Float(), required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_cpu_load_status(self, data, **kwargs):
        return ServerCPULoadStatus(**data)


# CPU status field of server status request response...
@attr.s
class ServerCPUStatus:
    cores                          = attr.ib()
    load                           = attr.ib()


# CPU status of server status request response schema...
class ServerCPUStatusSchema(Schema):

    # Fields...
    cores                           = fields.Integer(required=True)
    load                            = fields.Nested(ServerCPULoadStatusSchema(), required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_cpu_status(self, data, **kwargs):
        return ServerCPUStatus(**data)


# Disk field of server status request response...
@attr.s
class ServerDiskStatus:
    client_store_upload            = attr.ib()
    client_store_upload_directory  = attr.ib()
    available                      = attr.ib()
    capacity                       = attr.ib()


# Disk field of server status request response schema...
class ServerDiskStatusSchema(Schema):

    # Fields...
    client_store_upload             = fields.Bool(required=True)
    client_store_upload_directory   = fields.String(required=True)
    available                       = fields.Integer(required=True)
    capacity                        = fields.Integer(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_disk_status(self, data, **kwargs):
        return ServerDiskStatus(**data)


# Server status response...
@attr.s
class ServerStatus:
    algorithm_age   = attr.ib()
    built           = attr.ib()
    configured      = attr.ib()
    cpu             = attr.ib()
    disk            = attr.ib()
    encoding        = attr.ib()
    songs           = attr.ib()
    system          = attr.ib()
    uptime          = attr.ib()
    version         = attr.ib()


# Server status response schema...
class ServerStatusSchema(Schema):

    # Fields...
    algorithm_age   = fields.Integer(required=True)
    built           = fields.DateTime(required=True, format='rfc')
    configured      = fields.String(required=True)
    cpu             = fields.Nested(ServerCPUStatusSchema(), required=True)
    disk            = fields.Nested(ServerDiskStatusSchema(), required=True)
    encoding        = fields.String(required=True)
    songs           = fields.Integer(required=True)
    system          = fields.String(required=True)
    uptime          = fields.Integer(required=True)
    version         = fields.String(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_status(self, data, **kwargs):
        return ServerStatus(**data)

