from flask import Blueprint
from flask_restful import Api
from .resources.video import (
    VideoUploadResource,
    VideoDetailsResource,
    VideoListResource,
    VideoTrimResource,
    VideoMergeResource
)

# Create blueprint for v1 API
bp_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v1 = Api(bp_v1)

# Register routes
api_v1.add_resource(VideoListResource, '/videos')
api_v1.add_resource(VideoUploadResource, '/videos/upload')
api_v1.add_resource(VideoDetailsResource, '/videos/<string:video_id>')
api_v1.add_resource(VideoTrimResource, '/videos/<string:video_id>/trim')
api_v1.add_resource(VideoMergeResource, '/videos/merge')
# TODO:: Yet to define share schema
# api_v1.add_resource(TODO_DEFINE, '/videos/<string:video_id>/share')
# api_v1.add_resource(TODO_DEFINE, '/share/<string:token>')
