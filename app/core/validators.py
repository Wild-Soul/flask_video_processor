from typing import BinaryIO
from moviepy.editor import VideoFileClip
from .exceptions import ValidationError

class VideoValidator:
    """
    A class to validate video files according to specified criteria such as file size, 
    file extension, and video duration.

    Attributes:
        max_size (int): The maximum allowed size for the video file in bytes.
        min_duration (float): The minimum allowed duration for the video in seconds.
        max_duration (float): The maximum allowed duration for the video in seconds.
        allowed_extensions (set): A set of allowed file extensions for the video file.
    """

    def __init__(self, config):
        """
        Initializes the VideoValidator with the provided configuration settings.
        
        Args:
            config: A configuration object that provides the following attributes:
                - MAX_VIDEO_SIZE: The maximum file size allowed for the video.
                - MIN_VIDEO_DURATION: The minimum duration allowed for the video.
                - MAX_VIDEO_DURATION: The maximum duration allowed for the video.
                - ALLOWED_VIDEO_EXTENSIONS: A set of allowed video file extensions.
        """
        self.max_size = config.get('MAX_VIDEO_SIZE')
        self.min_duration = config.get('MIN_VIDEO_DURATION')
        self.max_duration = config.get('MAX_VIDEO_DURATION')
        self.allowed_extensions = config.get('ALLOWED_VIDEO_EXTENSIONS')

    def validate_file_size(self, file: BinaryIO) -> None:
        """
        Validates that the file size does not exceed the maximum allowed size.

        Args:
            file (BinaryIO): The video file to check the size of.
        
        Raises:
            ValidationError: If the file size exceeds the maximum allowed size.
        """
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        
        if size > self.max_size:
            raise ValidationError(
                f"File size exceeds maximum allowed size of {self.max_size/1024/1024}MB"
            )

    def validate_extension(self, filename: str) -> None:
        """
        Validates that the file extension is one of the allowed extensions.
        
        Args:
            filename (str): The name of the file to validate the extension of.
        
        Raises:
            ValidationError: If the file extension is not in the allowed extensions.
        """
        ext = filename.rsplit('.', 1)[-1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(
                f"File extension not allowed. Allowed extensions: {', '.join(self.allowed_extensions)}"
            )

    def validate_duration(self, file: BinaryIO) -> float:
        """
        Validates that the video duration is within the specified minimum and maximum duration.

        Args:
            file (BinaryIO): The video file to check the duration of.
        
        Returns:
            float: The duration of the video in seconds.
        
        Raises:
            ValidationError: If the video duration is shorter than the minimum duration 
                             or longer than the maximum duration.
        """
        try:
            video = VideoFileClip(file.name)
            duration = video.duration
            
            if duration < self.min_duration:
                raise ValidationError(
                    f"Video duration ({duration}s) is less than minimum allowed ({self.min_duration}s)"
                )
            
            if duration > self.max_duration:
                raise ValidationError(
                    f"Video duration ({duration}s) exceeds maximum allowed ({self.max_duration}s)"
                )
            
            return duration
        finally:
            if 'video' in locals():
                video.close()
