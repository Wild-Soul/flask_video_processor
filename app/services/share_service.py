from datetime import datetime, timedelta, timezone
from typing import Dict
from app.core.exceptions import ValidationError
from app.repositories.video_repository import VideoRepository
from app.repositories.share_repository import ShareRepository
from app.services.storage_service import StorageService

class ShareService:
    def __init__(
        self,
        config,
        video_repository: VideoRepository,
        share_repository: ShareRepository,
        storage_service: StorageService
    ):
        self.config = config
        self.video_repository = video_repository
        self.share_repository = share_repository
        self.storage_service = storage_service

    def create_share_link(self, video_id: int, expires_in: int = None) -> Dict:
        video = self.video_repository.get_by_id(video_id)
        if not video:
            raise ValidationError("Video not found")

        expires_in = expires_in or self.config.get('DEFAULT_SHARE_EXPIRY')
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        # Create share link
        share_link = self.share_repository.create_share_link(
            video_id=video_id,
            expires_at=expires_at
        )
        self.share_repository.commit()

        return {
            "token": share_link.token,
            "expires_at": expires_at.isoformat(),
            "video_id": video_id
        }

    def get_shared_video(self, token: str) -> Dict:
        share_link = self.share_repository.get_by_token(token)
        if not share_link:
            raise ValidationError("Invalid share link")

        if share_link.expires_at.tzinfo is None:
            # Convert naive expires_at to aware by assigning the UTC timezone
            share_link.expires_at = share_link.expires_at.replace(tzinfo=timezone.utc)
    
        if share_link.expires_at < datetime.now(timezone.utc):
            raise ValidationError("Share link has expired")

        video = self.video_repository.get_by_id(share_link.video_id)
        if not video:
            raise ValidationError("Video not found")

        # Generate temporary URL for video access
        # Calculate how much time is remaining till expiry only generate link for that time.
        delta =  share_link.expires_at - datetime.now(timezone.utc)
        video_url = self.storage_service.get_file_url(
            video.storage_path,
            expires=delta
        )

        return {
            "video_id": video.id,
            "filename": video.original_filename,
            "duration": video.duration,
            "size": video.file_size,
            "url": video_url,
            "expires_at": share_link.expires_at
        }
