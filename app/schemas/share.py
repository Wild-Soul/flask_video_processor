from marshmallow import Schema, fields
from .base import BaseResponseSchema

class ShareLinkCreateSchema(Schema):
    expires_in = fields.Int(required=False, description="Expiry time in minutes")

class ShareLinkSchema(Schema):
    token = fields.String(required=False)
    expires_at = fields.String(required=True)
    video_id = fields.UUID(required=True)
    url = fields.String(required=False)

class ShareLinkResponseSchema(BaseResponseSchema):
    data = fields.Nested(ShareLinkSchema)
