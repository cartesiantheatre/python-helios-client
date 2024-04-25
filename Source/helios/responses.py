#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# System imports...
import datetime

# Other imports...
import attr
from marshmallow import Schema, fields, post_load, EXCLUDE


# Server error response...
@attr.s
class Error:
    code    = attr.ib(validator=attr.validators.instance_of(int))
    details = attr.ib(validator=attr.validators.instance_of(str))
    summary = attr.ib(validator=attr.validators.instance_of(str))


# Server error response schema...
class ErrorSchema(Schema):

    # Don't raise a ValidationError on load() when server's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    code            = fields.Integer(required=True)
    details         = fields.String(required=True)
    summary         = fields.String(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_error(self, data, **kwargs):
        return Error(**data)


# Genre information...
@attr.s
class GenreInformation:
    genre               = attr.ib(validator=attr.validators.instance_of(str))
    count               = attr.ib(validator=attr.validators.instance_of(int))


# Genre information schema...
class GenreInformationSchema(Schema):

    # Don't raise a ValidationError on load() when server's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    genre               = fields.String(required=True)
    count               = fields.Integer(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_genre_information(self, data, **kwargs):
        return GenreInformation(**data)


# Learning example...
@attr.s
class LearningExample:
    anchor              = attr.ib(validator=attr.validators.instance_of(str))
    positive            = attr.ib(validator=attr.validators.instance_of(str))
    negative            = attr.ib(validator=attr.validators.instance_of(str))


# learning example schema...
class LearningExampleSchema(Schema):

    # Fields...
    anchor              = fields.String(allow_none=True)
    positive            = fields.String(allow_none=True)
    negative            = fields.String(allow_none=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_learning_example(self, data, **kwargs):
        return LearningExample(**data)


# Job status response...
@attr.s
class JobStatus:
    eta                 = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    message             = attr.ib(default='', validator=attr.validators.instance_of(str))
    progress_current    = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    progress_rate       = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    progress_total      = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))


# Job status response schema...
class JobStatusSchema(Schema):

    # Fields...
    eta                 = fields.Integer(required=False)
    message             = fields.String(required=True)
    progress_current    = fields.Integer(required=False)
    progress_rate       = fields.Integer(required=False)
    progress_total      = fields.Integer(required=False)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_error(self, data, **kwargs):
        return JobStatus(**data)


# Stored song response after adding, modifying, or retrieving a song...
@attr.s
class StoredSong:
    album               = attr.ib(validator=attr.validators.instance_of(str))
    algorithm_age       = attr.ib(validator=attr.validators.instance_of(int))
    artist              = attr.ib(validator=attr.validators.instance_of(str))
    beats_per_minute    = attr.ib(validator=attr.validators.instance_of(float))
    duration            = attr.ib(validator=attr.validators.instance_of(int))
    fingerprint         = attr.ib(validator=attr.validators.instance_of(str))
    genre               = attr.ib(validator=attr.validators.instance_of(str))
    id                  = attr.ib(validator=attr.validators.instance_of(int))
    isrc                = attr.ib(validator=attr.validators.instance_of(str))
    location            = attr.ib(validator=attr.validators.instance_of(str))
    reference           = attr.ib(validator=attr.validators.instance_of(str))
    title               = attr.ib(validator=attr.validators.instance_of(str))
    year                = attr.ib(validator=attr.validators.instance_of(int))


# Stored song response schema after adding, modifying, or retrieving a song...
class StoredSongSchema(Schema):

    # Don't raise a ValidationError on load() when server's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    album               = fields.String(required=True)
    algorithm_age       = fields.Integer(required=True)
    artist              = fields.String(required=True)
    beats_per_minute    = fields.Float(required=True)
    duration            = fields.Integer(required=True)
    fingerprint         = fields.String(required=False)
    genre               = fields.String(required=True)
    id                  = fields.Integer(required=True)
    isrc                = fields.String(required=True)
    location            = fields.String(required=True)
    reference           = fields.String(required=True)
    title               = fields.String(required=True)
    year                = fields.Integer(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_stored_song(self, data, **kwargs):
        return StoredSong(**data)


# CPU load status field of system's CPU status request response...
@attr.s
class SystemCPULoadStatus:
    all                             = attr.ib(validator=attr.validators.instance_of(float))
    individual                      = attr.ib()


# CPU load status field of system CPU status request response schema...
class SystemCPULoadStatusSchema(Schema):

    # Don't raise a ValidationError on load() when system's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    all                             = fields.Float(required=True)
    individual                      = fields.List(fields.Float(), required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_system_cpu_load_status(self, data, **kwargs):
        return SystemCPULoadStatus(**data)


# CPU status field of system's status request response...
@attr.s
class SystemCPUStatus:
    architecture                    = attr.ib(validator=attr.validators.instance_of(str))
    cores                           = attr.ib(validator=attr.validators.instance_of(int))
    load                            = attr.ib()


# CPU status of system status request response schema...
class SystemCPUStatusSchema(Schema):

    # Don't raise a ValidationError on load() when system's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    architecture                    = fields.String(required=True)
    cores                           = fields.Integer(required=True)
    load                            = fields.Nested(SystemCPULoadStatusSchema(), required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_system_cpu_status(self, data, **kwargs):
        return SystemCPUStatus(**data)


# Disk field of system status request response...
@attr.s
class SystemDiskStatus:
    client_store_upload            = attr.ib(validator=attr.validators.instance_of(bool))
    client_store_upload_directory  = attr.ib(default='', validator=attr.validators.optional(attr.validators.instance_of(str)))
    available                      = attr.ib(default=0, validator=attr.validators.optional(attr.validators.instance_of(int)))
    capacity                       = attr.ib(default=0, validator=attr.validators.optional(attr.validators.instance_of(int)))


# Disk field of system status request response schema...
class SystemDiskStatusSchema(Schema):

    # Don't raise a ValidationError on load() when system's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    client_store_upload             = fields.Bool(required=True)
    client_store_upload_directory   = fields.String(required=False)
    available                       = fields.Integer(required=False)
    capacity                        = fields.Integer(required=False)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_system_disk_status(self, data, **kwargs):
        return SystemDiskStatus(**data)


# Learning field of system status request response...
@attr.s
class SystemLearningStatus:
    examples                        = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
    last_trained                    = attr.ib(validator=attr.validators.instance_of(datetime.datetime))


# Learning field of system status request response schema...
class SystemLearningStatusSchema(Schema):

    # Don't raise a ValidationError on load() when system's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    examples                        = fields.Integer(required=True)
    last_trained                    = fields.DateTime(required=True, format='iso') # ISO 8601

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_system_learning_status(self, data, **kwargs):
        return SystemLearningStatus(**data)


# System status response...
@attr.s
class SystemStatus:
    algorithm_age   = attr.ib(validator=attr.validators.instance_of(int))
    built           = attr.ib(validator=attr.validators.instance_of(datetime.datetime))
    configured      = attr.ib(validator=attr.validators.instance_of(str))
    cpu             = attr.ib()
    disk            = attr.ib()
    encoding        = attr.ib(validator=attr.validators.instance_of(str))
    learning        = attr.ib()
    songs           = attr.ib(validator=attr.validators.instance_of(int))
    system          = attr.ib(validator=attr.validators.instance_of(str))
    tls             = attr.ib(validator=attr.validators.instance_of(bool))
    uptime          = attr.ib(validator=attr.validators.instance_of(int))
    version         = attr.ib(validator=attr.validators.instance_of(str))


# System status response schema...
class SystemStatusSchema(Schema):

    # Don't raise a ValidationError on load() when system's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    algorithm_age   = fields.Integer(required=True)
    built           = fields.DateTime(required=True, format='iso') # ISO 8601
    configured      = fields.String(required=True)
    cpu             = fields.Nested(SystemCPUStatusSchema(), required=True)
    disk            = fields.Nested(SystemDiskStatusSchema(), required=True)
    encoding        = fields.String(required=True)
    learning        = fields.Nested(SystemLearningStatusSchema(), required=True)
    songs           = fields.Integer(required=True)
    system          = fields.String(required=True)
    tls             = fields.Bool(required=True)
    uptime          = fields.Integer(required=True)
    version         = fields.String(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_system_status(self, data, **kwargs):
        return SystemStatus(**data)


# Training report response...
@attr.s
class TrainingReport:
    accuracy        = attr.ib(validator=attr.validators.instance_of(float))
    gpu_accelerated = attr.ib(validator=attr.validators.instance_of(bool))
    total_time      = attr.ib(validator=attr.validators.instance_of(int))


# Training report response schema...
class TrainingReportSchema(Schema):

    # Don't raise a ValidationError on load() when system's response contains
    #  new fields the client may not recognize yet...
    class Meta:
        unknown = EXCLUDE

    # Fields...
    accuracy        = fields.Float(required=True)
    gpu_accelerated = fields.Bool(required=True)
    total_time      = fields.Integer(required=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_training_report(self, data, **kwargs):
        return TrainingReport(**data)
