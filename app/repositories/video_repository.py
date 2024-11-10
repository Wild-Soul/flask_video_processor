from typing import List, Optional
from app.models.video import Video
from .base_repository import BaseRepository

class VideoRepository(BaseRepository[Video]):
    def __init__(self):
        super().__init__(Video)

    def get_videos_by_ids(self, video_ids: List[int]) -> List[Video]:
        return Video.query.filter(Video.id.in_(video_ids)).all()

    def get_by_storage_path(self, storage_path: str) -> Optional[Video]:
        return Video.query.filter_by(storage_path=storage_path).first()
