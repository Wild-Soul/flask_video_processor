from marshmallow import Schema, fields, validates

from app.core.exceptions import ValidationError
from .base import BaseResponseSchema

class VideoUploadSchema(Schema):
    # File validation is handled separately
    description = fields.String(required=False)
    tags = fields.List(fields.String(), required=False)

class VideoTrimSchema(Schema):
    start_time = fields.Float(required=True, validate=lambda n: n >= 0)
    end_time = fields.Float(required=True, validate=lambda n: n > 0)
    
    @validates('end_time')
    def validate_end_time(self, value, **kwargs):
        if value <= self.context.get('start_time', 0):
            raise ValidationError("end_time must be greater than start_time")

class VideoMergeSchema(Schema):
    # TODO:: Add validation, there should at-least be two ids to merge
    video_ids = fields.List(fields.String(), required=True, validate=lambda n: len(n) >= 2)
    output_format = fields.String(required=False, missing='mp4')

class VideoDetailsSchema(Schema):
    id = fields.String(required=True)
    filename = fields.String(required=True)
    original_filename = fields.String(required=True)
    duration = fields.Float(required=True)
    size = fields.Int(required=True)
    created_at = fields.String(required=True)
    metadata = fields.Dict(required=False)
    url = fields.String(required=False) # incase a share link is generated.

class VideoListResponseSchema(BaseResponseSchema):
    data = fields.Nested(VideoDetailsSchema, many=True)
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()

class VideoResponseSchema(BaseResponseSchema):
    data = fields.Nested(VideoDetailsSchema)
