from marshmallow import Schema, fields
from .base import BaseResponseSchema

class VideoUploadSchema(Schema):
    # File validation is handled separately
    description = fields.String(required=False)
    tags = fields.List(fields.String(), required=False)

class VideoTrimSchema(Schema):
    start_time = fields.Float(required=True, validate=lambda n: n >= 0)
    end_time = fields.Float(required=True, validate=lambda n: n > 0)
    
    #TODO:: Add validation for time, end_time > start_time.

class VideoMergeSchema(Schema):
    # TODO:: Add validation, there should at-least be two ids to merge
    video_ids = fields.List(fields.String(), required=True)
    output_format = fields.String(required=False, missing='mp4')

class VideoDetailsSchema(Schema):
    # WIP:: TODO:: Setting required to false for all fields, but that shouldn't be the case.
    id = fields.String(required=False)
    filename = fields.String(required=False)
    original_filename = fields.String(required=False)
    duration = fields.Float(required=False)
    size = fields.Int(required=False)
    created_at = fields.DateTime(required=False)
    metadata = fields.Dict(required=False) # any kind of meta information about the video, that we want to send.
    url = fields.String(required=False)

class VideoListResponseSchema(BaseResponseSchema):
    data = fields.Nested(VideoDetailsSchema, many=True)
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()

class VideoResponseSchema(BaseResponseSchema):
    data = fields.Nested(VideoDetailsSchema)
