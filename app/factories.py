from typing import Dict
from flask import Flask

from .services.share_service import ShareService
from .services.storage_service import StorageService
from .services.video_service import VideoService
from .repositories.video_repository import VideoRepository
from .repositories.share_repository import ShareRepository

class ServiceFactory:
    _instances: Dict = {}

    @classmethod
    def create_services(cls, app: Flask):
        """Create all service instances with their dependencies"""
        if not cls._instances:
            video_repo = VideoRepository()
            share_repo = ShareRepository()

            # Create services
            storage_service = StorageService(app.config)
            video_service = VideoService(app.config, video_repo, storage_service)
            share_service = ShareService(app.config, video_repo, share_repo, storage_service)


            # Store instances
            cls._instances = {
                'storage_service': storage_service,
                'video_service': video_service,
                'share_service': share_service,
            }

        return cls._instances

    @classmethod
    def get_service(cls, service_name: str):
        """Get a service instance by name"""
        if not cls._instances:
            raise RuntimeError("Services not initialized. Call create_services first.")
        return cls._instances.get(service_name)
