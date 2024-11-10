from flask import request, current_app
from flask_restful import Resource
from app.core.auth import require_auth
from app.core.exceptions import ValidationError
from app.schemas.video import (
    VideoUploadSchema,
    VideoTrimSchema,
    VideoMergeSchema,
    VideoListResponseSchema,
    VideoResponseSchema
)
from app.factories import ServiceFactory

class VideoBaseResource(Resource):
    def __init__(self):
        # TODO:: initialize video service here, i.e. get it from service_factory.
        pass

class VideoListResource(VideoBaseResource):
    @require_auth
    def get(self):
        """Get list of all videos"""
        schema = VideoListResponseSchema()
        
        return schema.dump({
            'success': True,
            'data': [],
            'total': 0,
            'page': 0,
            'per_page': 0
        })

class VideoUploadResource(VideoBaseResource):
    @require_auth
    def post(self):
        """Upload a new video"""
        if 'video' not in request.files:
            raise ValidationError('No video file provided')

        file = request.files['video']
        if not file.filename:
            raise ValidationError('No selected file')

        # Validate additional parameters
        schema = VideoUploadSchema()
        data = schema.load(request.form)


        response_schema = VideoResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': data
        })

class VideoDetailsResource(VideoBaseResource):
    @require_auth
    def get(self, video_id):
        """Get video details"""
        schema = VideoResponseSchema()
        return schema.dump({
            'success': True,
            'data': {
                "something": "for now"
            }
        })

    @require_auth
    def delete(self, video_id):
        """Delete a video"""
        return {'success': True, 'message': 'Video deleted successfully'}, 200

class VideoTrimResource(VideoBaseResource):
    @require_auth
    def post(self, video_id):
        """Trim a video"""
        schema = VideoTrimSchema()
        data = schema.load(request.get_json())
        
        response_schema = VideoResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': data
        })

class VideoMergeResource(VideoBaseResource):
    @require_auth
    def post(self):
        """Merge multiple videos"""
        schema = VideoMergeSchema()
        data = schema.load(request.get_json())
        
        result = self.video_service.merge_videos(
            data['video_ids'],
            output_format=data.get('output_format', 'mp4')
        )
        
        response_schema = VideoResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': result
        })
