from src.domain.entities.video_entity import VideoEntity
from src.adapters.driven.database.repositories.generic_repository import GenericORM
from sqlalchemy.orm import Session


class VideoRepository(GenericORM):
    __collection__ = "video"

    @classmethod
    def create_obj(cls, video: VideoEntity) -> VideoEntity:
        return cls.create(video, VideoEntity)

    @classmethod
    def list_all(cls) -> list[VideoEntity]:
        return cls.find_all(VideoEntity)

    @classmethod
    def get(cls, video_id: str) -> VideoEntity:
        return cls.find_by_id(video_id, VideoEntity)

    @classmethod
    def update(cls, video: VideoEntity) -> VideoEntity:
        return cls.save(video, VideoEntity)

    @classmethod
    def delete(cls, video_id: str) -> None:
        cls.delete_by_id(video_id)

    @classmethod
    def filter_obj(cls, syntax):
        return cls.filter(syntax, VideoEntity)
