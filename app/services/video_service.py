import tempfile
from typing import Dict, List
import moviepy.editor as mp
from werkzeug.datastructures import FileStorage
from app.core.validators import VideoValidator
from app.core.exceptions import VideoProcessingError
from app.repositories.video_repository import VideoRepository
from .storage_service import StorageService

class VideoService:
    def __init__(self, config, video_repository: VideoRepository, storage_service: StorageService):
        self.config = config
        self.validator = VideoValidator(config)
        self.video_repository = video_repository
        self.storage_service = storage_service
    
    def upload_video(self, file: FileStorage, filename: str) -> Dict:
        try:
            # Validate video
            self.validator.validate_file_size(file.stream)
            self.validator.validate_extension(filename)
            duration = self.validator.validate_duration(file.stream)
            file_size = file.content_length or 0  # Fallback to 0 if not available
            
            if file_size == 0:
                file.stream.seek(0, 2)
                file_size = file.stream.tell()
                file.stream.seek(0)

            # Generate storage path
            storage_path = self.storage_service.generate_storage_path(filename)
            file.stream.seek(0)
            
            self.storage_service.upload_file(
                file.stream,
                storage_path
            )

            # Create database entry
            video = self.video_repository.create(
                filename=storage_path.split('/')[-1],
                original_filename=filename,
                file_size=file_size,
                duration=duration,
                storage_path=storage_path
            )
            self.video_repository.commit()

            return {
                "id": video.id,
                "filename": filename,
                "duration": duration,
                "size": file_size
            }

        except Exception as e:
            self.video_repository.rollback()
            # Cleanup storage if needed
            try:
                self.storage_service.delete_file(storage_path)
            except:
                pass
            raise VideoProcessingError(f"Failed to process video: {str(e)}")
    
    def get_video_details(self, video_id: int) -> Dict:
        video = self.video_repository.get_by_id(video_id)
        if not video:
            raise VideoProcessingError("Video not found")

        return {
            "id": video.id,
            "filename": video.original_filename,
            "duration": video.duration,
            "size": video.file_size,
            "created_at": video.created_at.isoformat(),
            "meta": video.meta
        }

    def get_videos(self, page, per_page) -> Dict:
        limit = per_page
        offset = (page-1) * per_page
        videos = self.video_repository.get_all(limit=limit, offset=offset)

        videos_map = [{
            "id": v.id,
            "filename": v.original_filename,
            "duration": v.duration,
            "size": v.file_size,
            "created_at": v.created_at.isoformat(),
            "meta": v.meta
        } for v in videos]

        total = self.video_repository.count()
        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "data": videos_map,
        }

    def trim_video(self, video_id: int, start_time: float, end_time: float) -> Dict:
        """
        Trims video and uploads it to minio.
        It doesn't replaces the orignal video, in order to keep a history of modifications.
        This can be improved further by marking a video ready to be gc(background worker) collected, maybe every 48 hours.
        """
        video = self.video_repository.get_by_id(video_id)
        if not video:
            raise VideoProcessingError("Video not found")

        try:
            # Create temporary file for processing
            with tempfile.NamedTemporaryFile(suffix='.mp4') as temp_file:
                # Download original video
                original_url = self.storage_service.get_file_url(video.storage_path)
                clip = mp.VideoFileClip(original_url)
                
                # Trim video
                trimmed = clip.subclip(start_time, end_time)
                trimmed.write_videofile(temp_file.name)
                
                # Upload trimmed video
                storage_path = self.storage_service.generate_storage_path(f"trimmed_{video.filename}")
                with open(temp_file.name, 'rb') as f:
                    self.storage_service.upload_file(f, storage_path)
                
                # Create new video entry
                # TODO:: This should be coming from user, if not provided default to a naming convention like right now.
                new_video = self.video_repository.create(
                    filename=storage_path.split('/')[-1],
                    original_filename=f"trimmed_{video.original_filename}",
                    file_size=temp_file.tell(),
                    duration=end_time - start_time,
                    storage_path=storage_path,
                    metadata={"source_video_id": video_id}
                )
                self.video_repository.commit()

                return {
                    "id": new_video.id,
                    "filename": new_video.filename,
                    "duration": new_video.duration,
                    "size": new_video.file_size
                }

        except Exception as e:
            self.video_repository.rollback()
            raise VideoProcessingError(f"Failed to trim video: {str(e)}")

    def merge_videos(self, video_ids: List[int], output_format: str = 'mp4') -> Dict:
        videos = self.video_repository.get_videos_by_ids(video_ids)
        if len(videos) != len(video_ids):
            raise VideoProcessingError("One or more videos not found")

        try:
            # Create temporary file for processing
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}') as temp_file:
                # Download and process all videos
                clips = []
                for video in videos:
                    url = self.storage_service.get_file_url(video.storage_path)
                    clips.append(mp.VideoFileClip(url))

                # Merge videos
                final_clip = mp.concatenate_videoclips(clips)

                # Get codec, choosing codec based outfile file extension.
                codec_map = self.config.get('EXTENSION_CODE_MAP', {})
                codec = codec_map.get(output_format, 'libx264')
                final_clip.write_videofile(temp_file.name, codec=codec)

                # Upload merged video
                # TODO:: Storage path should be coming from user, optinally.
                storage_path = self.storage_service.generate_storage_path("merged_video.mp4")
                with open(temp_file.name, 'rb') as f:
                    self.storage_service.upload_file(f, storage_path)

                # Create new video entry
                new_video = self.video_repository.create(
                    filename=storage_path.split('/')[-1],
                    original_filename="merged_video.mp4",
                    file_size=temp_file.tell(),
                    duration=final_clip.duration,
                    storage_path=storage_path,
                    metadata={"source_video_ids": video_ids}
                )
                self.video_repository.commit()

                # Cleanup
                for clip in clips:
                    clip.close()
                final_clip.close()

                return {
                    "id": new_video.id,
                    "filename": new_video.filename,
                    "duration": new_video.duration,
                    "size": new_video.file_size
                }

        except Exception as e:
            self.video_repository.rollback()
            raise VideoProcessingError(f"Failed to merge videos: {str(e)}")