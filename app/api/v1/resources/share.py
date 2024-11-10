from flask import request
from flask_restful import Resource
from app.core.auth import require_auth
from app.schemas.share import (
    ShareLinkCreateSchema,
    ShareLinkResponseSchema
)
from app.factories import ServiceFactory

class ShareBaseResource(Resource):
    def __init__(self):
         # TODO:: initialize share service here, i.e. get it from service_factory.
        pass

class ShareLinkResource(ShareBaseResource):
    @require_auth
    def post(self, video_id):
        """Create a share link for a video"""
        schema = ShareLinkCreateSchema()
        data = schema.load(request.get_json() or {})
        
        response_schema = ShareLinkResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': {
                'video_id': video_id
            }
        })

class SharedVideoResource(ShareBaseResource):
    def get(self, token):
        """Get shared video details"""
        
        response_schema = ShareLinkResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': {"something": "for now"}
        })
