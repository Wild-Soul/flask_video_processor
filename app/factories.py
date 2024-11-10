from typing import Dict
from flask import Flask
from .services.storage_service import StorageService
from .services.video_service import VideoService
from .repositories.video_repository import VideoRepository

class ServiceFactory:
    _instances: Dict = {}

    @classmethod
    def create_services(cls, app: Flask):
        """Create all service instances with their dependencies"""
        if not cls._instances:
            video_repo = VideoRepository()

            # Create services
            storage_service = StorageService(app.config)
            video_service = VideoService(app.config, video_repo, storage_service)

            # Store instances
            cls._instances = {
                'storage_service': storage_service,
                'video_service': video_service,
            }

        return cls._instances

    @classmethod
    def get_service(cls, service_name: str):
        """Get a service instance by name"""
        if not cls._instances:
            raise RuntimeError("Services not initialized. Call create_services first.")
        return cls._instances.get(service_name)
