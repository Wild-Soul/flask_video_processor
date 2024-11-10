from marshmallow import Schema, fields
from .base import BaseResponseSchema

class ShareLinkCreateSchema(Schema):
    expires_in = fields.Int(required=False, description="Expiry time in hours")

class ShareLinkSchema(Schema):
    token = fields.String(required=False)
    expires_at = fields.DateTime(required=False)
    video_id = fields.UUID(required=False)
    url = fields.String(required=False)

class ShareLinkResponseSchema(BaseResponseSchema):
    data = fields.Nested(ShareLinkSchema)
