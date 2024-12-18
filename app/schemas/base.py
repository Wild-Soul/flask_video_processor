from marshmallow import Schema, fields

class PaginationSchema(Schema):
    # TODO:: Check on adding validation to marshmallow. Page >=0 and per_page >= 10
    page = fields.Int(required=False, missing=1, strict=True)
    per_page = fields.Int(required=False, missing=20, strict=True)

class BaseResponseSchema(Schema):
    success = fields.Boolean(default=True)
    message = fields.String(required=False)
