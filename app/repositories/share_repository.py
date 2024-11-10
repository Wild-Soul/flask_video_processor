import uuid
from datetime import datetime, timezone
from typing import Optional
from app.models.video import ShareLink
from .base_repository import BaseRepository

class ShareRepository(BaseRepository[ShareLink]):
    def __init__(self):
        super().__init__(ShareLink)

    def get_by_token(self, token: str) -> Optional[ShareLink]:
        return ShareLink.query.filter_by(token=token).first()

    def get_active_share(self, video_id: int) -> Optional[ShareLink]:
        return ShareLink.query.filter(
            ShareLink.video_id==video_id,
            ShareLink.expires_at > datetime.now(timezone.utc)
        ).first()

    def create_share_link(self, video_id: int, expires_at: datetime) -> ShareLink:
        token = str(uuid.uuid4())
        return self.create(
            video_id=video_id,
            token=token,
            expires_at=expires_at
        )
