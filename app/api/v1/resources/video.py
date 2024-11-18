from flask import request
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_restful import Resource
from app.core.auth import require_auth
from app.core.exceptions import ValidationError
from app.schemas.video import (
    VideoListQuerySchema,
    VideoUploadSchema,
    VideoTrimSchema,
    VideoMergeSchema,
    VideoListResponseSchema,
    VideoResponseSchema
)
from app.factories import ServiceFactory
from app.services.video_service import VideoService

class VideoBaseResource(Resource, MethodResource):
    def __init__(self):
        self.video_service: VideoService = ServiceFactory.get_service('video_service')
        pass

@doc(tags=['Videos'])
class VideoListResource(VideoBaseResource):
    @require_auth
    @doc(description='Get list of all videos')
    @use_kwargs(VideoListQuerySchema, location='query')
    @marshal_with(VideoListResponseSchema)
    @marshal_with(VideoBaseResource)
    def get(self, page, per_page):
        '''Get list of all videos'''
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        response = self.video_service.get_videos(page, per_page)
        schema = VideoListResponseSchema()

        return schema.dump({
            'success': True,
            'data': response.get('data'),
            'total': response.get('total'),
            'page': response.get('page'),
            'per_page': response.get('per_page')
        })

@doc(tags=['Videos'])
class VideoUploadResource(VideoBaseResource):
    @require_auth
    @doc(description='Upload a new video file')
    @use_kwargs(VideoUploadSchema)
    @marshal_with(VideoResponseSchema)
    @marshal_with(VideoBaseResource)
    def post(self):
        '''Upload a new video'''
        if 'video' not in request.files:
            raise ValidationError('No video file provided')

        file = request.files['video']
        if not file.filename:
            raise ValidationError('No selected file')

         # Validate additional parameters
        schema = VideoUploadSchema()
        # TODO:: add meta support
        data = schema.load(request.form)

        # Process the upload
        result = self.video_service.upload_video(file, file.filename)

        response_schema = VideoResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': result
        })

@doc(tags=['Videos'])
class VideoDetailsResource(VideoBaseResource):
    @require_auth
    @doc(description='Get video details')
    @marshal_with(VideoResponseSchema)
    @marshal_with(VideoBaseResource)
    def get(self, video_id):
        '''Get video details'''
        video = self.video_service.get_video_details(video_id)
        schema = VideoResponseSchema()
        return schema.dump({
            'success': True,
            'data': video
        })

    @require_auth
    def delete(self, video_id):
        '''Delete a video'''
        self.video_service.delete(video_id)
        return {'success': True, 'message': 'Video deleted successfully'}, 200

@doc(tags=['Videos'])
class VideoTrimResource(VideoBaseResource):
    @require_auth
    @doc(description='Trim a video')
    @use_kwargs(VideoTrimSchema)
    @marshal_with(VideoResponseSchema)
    @marshal_with(VideoBaseResource)
    def post(self, video_id, start_time, end_time):
        '''Trim a video'''

        result = self.video_service.trim_video(
            video_id,
            start_time,
            end_time
        )
        
        response_schema = VideoResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': result
        })

@doc(tags=['Videos'])
class VideoMergeResource(VideoBaseResource):
    @require_auth
    @doc(description='Merge multiple videos')
    @use_kwargs(VideoMergeSchema)
    @marshal_with(VideoResponseSchema)
    @marshal_with(VideoBaseResource)
    def post(self, video_ids, output_format):
        '''Merge multiple videos'''
        
        result = self.video_service.merge_videos(
            video_ids,
            output_format
        )
        
        response_schema = VideoResponseSchema()
        return response_schema.dump({
            'success': True,
            'data': result
        })
