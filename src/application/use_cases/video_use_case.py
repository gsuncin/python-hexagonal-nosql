import tempfile
from src.infrastructure.logging.logger import logger
from src.domain.interfaces.video_interface import VideoInterface
from src.domain.entities.video_entity import VideoEntity
from src.core import settings
from smart_open import open
from io import BytesIO
import zipfile
import cv2
import os


class VideoUseCases:

    def __init__(self, video_repo: VideoInterface, auth_service=None):
        self.video_repo = video_repo
        self.auth = auth_service

    def create_video(self, video: VideoEntity):
        video.status = "pending"
        video.is_processed = False
        return self.video_repo.create_obj(video)

    def get_video(self, video_id: str) -> VideoEntity:
        return self.video_repo.get(video_id)

    def update_video(self, video: VideoEntity):
        return self.video_repo.update(video)

    def delete_video(self, video_id: str):
        self.video_repo.delete(video_id)

    def list_videos(self) -> list[VideoEntity]:
        return self.video_repo.list_all()

    def filter_videos(self, syntax: dict) -> list[VideoEntity]:
        return self.video_repo.filter_obj(syntax)

    def filter_videos_to_process(self, syntax: dict) -> list[VideoEntity]:
        syntax["is_processed"] = False
        syntax["status"] = "pending"
        return self.video_repo.filter_obj(syntax)

    def process_video(self, video: VideoEntity) -> VideoEntity:
        try:
            logger.info(f"Processing:{video.external_id} - path:{video.video_input}")
            video.status = "processing"
            self.video_repo.update(video)

            video_output = f"{video.video_input.split('.')[0]}_frames.zip"
            video_stream = self.__get_file(video.video_input)
            frames = self.__extract_frames_from_video(video_stream)
            zip_buffer = self.__zip_frames(frames)
            self.__save_file(video_output, zip_buffer)

            video.is_processed = True
            video.status = "completed"
            video.processed_output = video_output
            self.video_repo.update(video)
            logger.info(f"Saved processed frames to: {video_output}")
            return video

        except Exception as e:
            logger.error(f"Error processing video {video.external_id}: {e}")
            video.status = "error"
            self.video_repo.update(video)
            return video

    def __get_file(self, path: str) -> bytes:
        logger.info(f"Fetching file from path: {path}")
        transport = {}

        if not settings.CLOUD_ENABLED:
            transport = {"session": settings.CLOUD_SESSION}

        with open(path, "rb", transport_params=transport) as file:
            return file.read()

    def __save_file(self, path: str, data: bytes) -> None:
        logger.info(f"Saving file to path: {path}")
        transport = {}

        if not settings.CLOUD_ENABLED:
            transport = {"session": settings.CLOUD_SESSION}

        with open(path, "wb", transport_params=transport) as file:
            data = data.read()
            return file.write(data)

    def __zip_frames(self, frames: list[bytes]) -> BytesIO:
        logger.info(f"Creating zip buffer with {len(frames)} frames.")
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for idx, frame in enumerate(frames):
                zip_file.writestr(f"frame_{idx+1}.jpg", frame)
        zip_buffer.seek(0)
        return zip_buffer

    def __extract_frames_from_video(self, video_stream):
        logger.info("Extracting frames from video stream.")
        with tempfile.NamedTemporaryFile(
            suffix=".mp4", delete=False
        ) as temp_video_file:
            logger.info(f"temporary file stream: {temp_video_file.name}")
            temp_video_file.write(video_stream)
            temp_file_path = temp_video_file.name

        cap = cv2.VideoCapture(temp_file_path)
        frames = []
        max_frames = 10 # todo change to obj value
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = max(1, frame_count // max_frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        count = 0
        success, frame = cap.read()
        while success:
            if count % frame_interval == 0:
                _, jpeg_frame = cv2.imencode(".jpg", frame)
                frames.append(jpeg_frame.tobytes())
            count += 1
            success, frame = cap.read()
        cap.release()

        logger.info(f"Removed temporary file: {temp_file_path}")
        os.remove(temp_file_path)
        return frames
