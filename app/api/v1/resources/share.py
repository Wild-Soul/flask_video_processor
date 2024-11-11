from flask import request
from flask_restful import Resource
from flask_apispec import MethodResource, marshal_with, doc
from app.core.auth import require_auth
from app.schemas.share import (
    ShareLinkCreateSchema,
    ShareLinkResponseSchema
)
from app.factories import ServiceFactory

class ShareBaseResource(Resource, MethodResource):
    def __init__(self):
        self.share_service = ServiceFactory.get_service('share_service')
        pass
@doc(tags=['Share'])
class ShareLinkResource(ShareBaseResource):
    @require_auth
    @doc(description='Get token to share a video.')
    @marshal_with(ShareLinkResponseSchema)
    @marshal_with(ShareBaseResource)
    def post(self, video_id):
        """Create a share link for a video"""
        schema = ShareLinkCreateSchema()
        data = schema.load(request.get_json() or {})
        
        result = self.share_service.create_share_link(
            video_id,
            expires_in=data.get('expires_in')
        )

        response_schema = ShareLinkResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': result
        })

class SharedVideoResource(ShareBaseResource):
    @require_auth
    @doc(description='Get presigned url for previously shared video.')
    @marshal_with(ShareLinkResponseSchema)
    @marshal_with(ShareBaseResource)
    def get(self, token):
        """Get shared video details"""
        result = self.share_service.get_shared_video(token)
        
        response_schema = ShareLinkResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': result
        })
