#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# Imports...
import attr
from marshmallow import Schema, fields, post_load
from helios.responses import LearningExample, LearningExampleSchema

# i18n...
import gettext
_ = gettext.gettext

# New song request...
@attr.s
class NewSong:
    album               = attr.ib(default=None)
    artist              = attr.ib(default=None)
    beats_per_minute    = attr.ib(default=None)
    file                = attr.ib(default=None)
    genre               = attr.ib(default=None)
    isrc                = attr.ib(default=None)
    reference           = attr.ib(default=None)
    title               = attr.ib(default=None)
    year                = attr.ib(default=None)


# New song schema request...
class NewSongSchema(Schema):

    # Fields...
    album               = fields.String(allow_none=True)
    artist              = fields.String(allow_none=True)
    beats_per_minute    = fields.Float(allow_none=True)
    file                = fields.String(allow_none=False, required=True)
    genre               = fields.String(allow_none=True)
    isrc                = fields.String(allow_none=True)
    reference           = fields.String(allow_none=False, required=True)
    title               = fields.String(allow_none=True)
    year                = fields.Integer(allow_none=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_new_song(self, data, **kwargs):
        return NewSong(**data)


# Patch song for modifying an existing song request...
@attr.s
class PatchSong:
    album               = attr.ib(default=None)
    artist              = attr.ib(default=None)
    beats_per_minute    = attr.ib(default=None)
    file                = attr.ib(default=None)
    genre               = attr.ib(default=None)
    isrc                = attr.ib(default=None)
    reference           = attr.ib(default=None)
    title               = attr.ib(default=None)
    year                = attr.ib(default=None)


# Patch song schema for modifying an existing song request...
class PatchSongSchema(Schema):

    # Fields...
    album               = fields.String(allow_none=True)
    artist              = fields.String(allow_none=True)
    beats_per_minute    = fields.Float(allow_none=True)
    file                = fields.String(allow_none=True)
    genre               = fields.String(allow_none=True)
    isrc                = fields.String(allow_none=True)
    reference           = fields.String(allow_none=True)
    title               = fields.String(allow_none=True)
    year                = fields.Integer(allow_none=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_patch_song(self, data, **kwargs):
        return PatchSong(**data)


# Perform training request...
@attr.s
class PerformTraining:
    pass


# Perform training schema request...
class PerformTrainingSchema(Schema):

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_perform_training(self, data, **kwargs):
        return PerformTraining(**data)


# Perform triplet mining request...
@attr.s
class PerformTripletMining:
    search_reference    = attr.ib(default=None)
    system_rankings     = attr.ib(default=None)
    user_rankings       = attr.ib(default=None)


# Perform triplet mining schema request...
class PerformTripletMiningSchema(Schema):

    # Fields...
    search_reference    = fields.String(allow_none=False, required=True)
    system_rankings     = fields.List(fields.String(allow_none=False, required=True))
    user_rankings       = fields.List(fields.String(allow_none=False, required=True))

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_perform_triplet_mining(self, data, **kwargs):
        return PerformTripletMining(**data)


# Similarity search request...
@attr.s
class SimilaritySearch:
    similar_file            = attr.ib(default=None)
    similar_id              = attr.ib(default=None)
    similar_reference       = attr.ib(default=None)
    similar_url             = attr.ib(default=None)
    same_genre              = attr.ib(default=None)
    maximum_results         = attr.ib(default=None)


# Similarity search schema request...
class SimilaritySearchSchema(Schema):

    # Fields...
    similar_file            = fields.String(allow_none=True)
    similar_id              = fields.Integer(allow_none=True)
    similar_reference       = fields.String(allow_none=True)
    similar_url             = fields.String(allow_none=True)
    same_genre              = fields.Boolean(allow_none=True)
    maximum_results         = fields.Integer(allow_none=True)

    # Callback to receive dictionary of deserialized data...
    @post_load
    def make_similarity_search(self, data, **kwargs):
        return SimilaritySearch(**data)
