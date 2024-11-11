from flask import Blueprint
from flask_restful import Api
from flask_apispec import FlaskApiSpec

from .resources.video import (
    VideoUploadResource,
    VideoDetailsResource,
    VideoListResource,
    VideoTrimResource,
    VideoMergeResource
)
from .resources.share import ShareLinkResource, SharedVideoResource

# Create blueprint for v1 API
bp_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v1 = Api(bp_v1)

# Register routes
api_v1.add_resource(VideoListResource, '/videos', endpoint='video_list')
api_v1.add_resource(VideoUploadResource, '/videos/upload', endpoint='video_upload')
api_v1.add_resource(VideoDetailsResource, '/videos/<string:video_id>', endpoint='video_details')
api_v1.add_resource(VideoTrimResource, '/videos/<string:video_id>/trim', endpoint='video_trim')
api_v1.add_resource(VideoMergeResource, '/videos/merge', endpoint='video_merge')
api_v1.add_resource(ShareLinkResource, '/videos/<string:video_id>/share', endpoint='share_link')
api_v1.add_resource(SharedVideoResource, '/share/<string:token>', endpoint='shared_video')

# Swagger ui
def register_docs(docs: FlaskApiSpec):
    """Register all resources with API docs."""
    # Register using view names instead of classes
    docs.register(VideoListResource, endpoint='video_list', blueprint='api_v1')
    docs.register(VideoUploadResource, endpoint='video_upload', blueprint='api_v1')
    docs.register(VideoDetailsResource, endpoint='video_details', blueprint='api_v1')
    docs.register(VideoTrimResource, endpoint='video_trim', blueprint='api_v1')
    docs.register(VideoMergeResource, endpoint='video_merge', blueprint='api_v1')
    docs.register(ShareLinkResource, endpoint='share_link', blueprint='api_v1')
    docs.register(SharedVideoResource, endpoint='shared_video', blueprint='api_v1')