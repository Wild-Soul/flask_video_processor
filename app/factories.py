from typing import Dict
from flask import Flask

class ServiceFactory:
    _instances: Dict = {}

    @classmethod
    def create_services(cls, app: Flask):
        """Create all service instances with their dependencies"""
        if not cls._instances:

            # TODO:: Store instances of different services that are needed (singleton pattern).
            cls._instances = {
            }

        return cls._instances

    @classmethod
    def get_service(cls, service_name: str):
        """Get a service instance by name"""
        if not cls._instances:
            raise RuntimeError("Services not initialized. Call create_services first.")
        return cls._instances.get(service_name)
