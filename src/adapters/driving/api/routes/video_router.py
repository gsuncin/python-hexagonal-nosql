from src.adapters.driven.database.repositories.video_repository import VideoRepository
from src.application.use_cases.video_use_case import VideoUseCases
from src.domain.entities.video_entity import VideoEntity
from src.adapters.driving.api.routes.base import token_jwt
from src.adapters.driven.database.base import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


def get_video_use_case() -> VideoUseCases:
    video_repo = VideoRepository()
    return VideoUseCases(video_repo)


@router.post("/video_create", tags=["Video"])
async def create_video(request: VideoEntity, db: Session = Depends(get_db)):
    video_use_case = get_video_use_case()
    video = video_use_case.create_video(request)
    video_use_case.process_video(video)
    return video


@router.get("/video_list", tags=["Video"])
async def list_videos(db: Session = Depends(get_db)):
    video_use_case = get_video_use_case()
    return video_use_case.list_videos()


@router.get("/video/{video_id}", tags=["Video"])
async def get_video(video_id: str, db: Session = Depends(get_db)):
    # async def get_video(token: token_jwt, video_id: str, db: Session = Depends(get_db)):
    video_use_case = get_video_use_case()
    return video_use_case.get_video(video_id)
