from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.video_entity import VideoEntity


class VideoInterface(ABC):
    @abstractmethod
    def create_obj(self, video: VideoEntity) -> VideoEntity: ...

    @abstractmethod
    def list_all(self) -> List[VideoEntity]: ...

    @abstractmethod
    def get(self, video_id: str) -> VideoEntity: ...

    @abstractmethod
    def update(self, video: VideoEntity) -> VideoEntity: ...

    @abstractmethod
    def delete(self, video_id: str) -> bool: ...

    @abstractmethod
    def filter_obj(self, syntax) -> List[VideoEntity]: ...

    @abstractmethod
    def to_dict(self) -> dict: ...

    @abstractmethod
    def process_video(self, video: VideoEntity) -> VideoEntity: ...