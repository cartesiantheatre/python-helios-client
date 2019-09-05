#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
import attr
import datetime
from marshmallow import Schema, fields, post_load

# Stored song response after adding, modifying, or retrieving a song...
@attr.s
class StoredSong:
    album           = attr.ib(validator=attr.validators.instance_of(str))
    algorithm_age   = attr.ib(validator=attr.validators.instance_of(int))
    artist          = attr.ib(validator=attr.validators.instance_of(str))
    duration        = attr.ib(validator=attr.validators.instance_of(int))
    genre           = attr.ib(validator=attr.validators.instance_of(str))
    id              = attr.ib(validator=attr.validators.instance_of(int))
    isrc            = attr.ib(validator=attr.validators.instance_of(str))
    location        = attr.ib(validator=attr.validators.instance_of(str))
    reference       = attr.ib(validator=attr.validators.instance_of(str))
    title           = attr.ib(validator=attr.validators.instance_of(str))
    year            = attr.ib(validator=attr.validators.instance_of(int))


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
    code    = attr.ib(validator=attr.validators.instance_of(int))
    details = attr.ib(validator=attr.validators.instance_of(str))
    summary = attr.ib(validator=attr.validators.instance_of(str))


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
    all                            = attr.ib(validator=attr.validators.instance_of(float))
    individual                     = attr.ib()


# CPU load status field of server CPU status request response schema...
class ServerCPULoadStatusSchema(Schema):

    # Fields...
    all                            = fields.Float(required=True)
    individual                     = fields.List(fields.Float(), required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_cpu_load_status(self, data, **kwargs):
        return ServerCPULoadStatus(**data)


# CPU status field of server status request response...
@attr.s
class ServerCPUStatus:
    cores                          = attr.ib(validator=attr.validators.instance_of(int))
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
    client_store_upload            = attr.ib(validator=attr.validators.instance_of(bool))
    client_store_upload_directory  = attr.ib(default='', validator=attr.validators.optional(attr.validators.instance_of(str)))
    available                      = attr.ib(default=0, validator=attr.validators.optional(attr.validators.instance_of(int)))
    capacity                       = attr.ib(default=0, validator=attr.validators.optional(attr.validators.instance_of(int)))


# Disk field of server status request response schema...
class ServerDiskStatusSchema(Schema):

    # Fields...
    client_store_upload             = fields.Bool(required=True)
    client_store_upload_directory   = fields.String(required=False)
    available                       = fields.Integer(required=False)
    capacity                        = fields.Integer(required=False)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_server_disk_status(self, data, **kwargs):
        return ServerDiskStatus(**data)


# Server status response...
@attr.s
class ServerStatus:
    algorithm_age   = attr.ib(validator=attr.validators.instance_of(int))
    built           = attr.ib(validator=attr.validators.instance_of(datetime.datetime))
    configured      = attr.ib(validator=attr.validators.instance_of(str))
    cpu             = attr.ib()
    disk            = attr.ib()
    encoding        = attr.ib(validator=attr.validators.instance_of(str))
    songs           = attr.ib(validator=attr.validators.instance_of(int))
    system          = attr.ib(validator=attr.validators.instance_of(str))
    uptime          = attr.ib(validator=attr.validators.instance_of(int))
    version         = attr.ib(validator=attr.validators.instance_of(str))


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

