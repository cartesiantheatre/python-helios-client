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
class StoredSongResponse:
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
class StoredSongResponseSchema(Schema):

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
    def make_stored_song_response(self, data, **kwargs):
        return StoredSongResponse(**data)


# Server error response...
@attr.s
class ErrorResponse:
    code    = attr.ib()
    details = attr.ib()
    summary = attr.ib()


# Server error response schema...
class ErrorResponseSchema(Schema):

    # Fields...
    code            = fields.Integer(required=True)
    details         = fields.String(required=True)
    summary         = fields.String(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_error_response(self, data, **kwargs):
        return ErrorResponse(**data)


# Disk field of on server status request response...
@attr.s
class ServerDiskStatus:
    client_store_upload            = attr.ib()
    client_store_upload_directory  = attr.ib()
    available                      = attr.ib()
    capacity                       = attr.ib()

# Disk field of on server status request response schema...
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
class ServerStatusResponse:
    algorithm_age   = attr.ib()
    built           = attr.ib()
    disk            = attr.ib()
    configured      = attr.ib()
    encoding        = attr.ib()
    songs           = attr.ib()
    system          = attr.ib()
    uptime          = attr.ib()
    version         = attr.ib()


# Server status response schema...
class ServerStatusResponseSchema(Schema):

    # Fields...
    algorithm_age   = fields.Integer(required=True)
    built           = fields.DateTime(required=True, format='rfc')
    disk            = fields.Nested(ServerDiskStatusSchema(), required=True)
    configured      = fields.String(required=True)
    encoding        = fields.String(required=True)
    songs           = fields.Integer(required=True)
    system          = fields.String(required=True)
    uptime          = fields.Integer(required=True)
    version         = fields.String(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_status_response(self, data, **kwargs):
        return ServerStatusResponse(**data)

