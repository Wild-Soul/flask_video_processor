import tempfile
from typing import BinaryIO, Dict
import moviepy.editor as mp
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

    def upload_video(self, file: BinaryIO, filename: str) -> Dict:
        try:
            # Validate video
            self.validator.validate_file_size(file)
            self.validator.validate_extension(filename)
            duration = self.validator.validate_duration(file)

            # Generate storage path and upload
            storage_path = self.storage_service.generate_storage_path(filename)
            self.storage_service.upload_file(file, storage_path)

            # Create database entry
            video = self.video_repository.create(
                filename=storage_path.split('/')[-1],
                original_filename=filename,
                file_size=file.tell(),
                duration=duration,
                storage_path=storage_path
            )
            self.video_repository.commit()

            return {
                "id": video.id,
                "filename": filename,
                "duration": duration,
                "size": file.tell()
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
