#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Imports...
import attr
from marshmallow import Schema, fields, post_load, pre_dump

# i18n...
import gettext
_ = gettext.gettext

# New song...
@attr.s
class NewSong(object):
    album       = attr.ib(default=None)
    artist      = attr.ib(default=None)
    file        = attr.ib(default=None)
    genre       = attr.ib(default=None)
    isrc        = attr.ib(default=None)
    reference   = attr.ib(default=None)
    title       = attr.ib(default=None)
    year        = attr.ib(default=None)

# New song schema...
class NewSongSchema(Schema):

    # Fields...
    album       = fields.String(allow_none=True)
    artist      = fields.String(allow_none=True)
    file        = fields.String(allow_none=False, required=True)
    genre       = fields.String(allow_none=True)
    isrc        = fields.String(allow_none=True)
    reference   = fields.String(allow_none=False, required=True)
    title       = fields.String(allow_none=True)
    year        = fields.Integer(allow_none=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_new_song(self, data, **kwargs):
        return NewSong(**data)

# Patch song for modifying an existing song...
@attr.s
class PatchSong:
    album       = attr.ib(default=None)
    artist      = attr.ib(default=None)
    file        = attr.ib(default=None)
    genre       = attr.ib(default=None)
    isrc        = attr.ib(default=None)
    reference   = attr.ib(default=None)
    title       = attr.ib(default=None)
    year        = attr.ib(default=None)

# Patch song schema for modifying an existing song...
class PatchSongSchema(Schema):

    # Fields...
    album           = fields.String(allow_none=True)
    artist          = fields.String(allow_none=True)
    file            = fields.String(allow_none=True)
    genre           = fields.String(allow_none=True)
    isrc            = fields.String(allow_none=True)
    reference       = fields.String(allow_none=True)
    title           = fields.String(allow_none=True)
    year            = fields.Integer(allow_none=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_patch_song(self, data, **kwargs):
        return PatchSong(**data)

