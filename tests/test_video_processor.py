from uuid import uuid4
from src.core import settings
from src.domain.entities.video_entity import VideoEntity
from src.adapters.driven.database.repositories.video_repository import VideoRepository
from src.application.use_cases.video_use_case import VideoUseCases
from tests.base import BaseTestSetupConfig, TestConfig
import unittest


class VideoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = TestConfig(use_database=True, delete_after_completed=True)
        cls.setup = BaseTestSetupConfig(config)
        cls.use_cases = cls.__get_use_case()
        cls.created_objects = []
        cls.email = "test@example.com"

    @classmethod
    def __get_use_case(cls) -> VideoUseCases:
        video_repo = VideoRepository()
        return VideoUseCases(video_repo)

    @classmethod
    def tearDownClass(cls):
        if cls.setup.config.delete_after_completed and cls.setup.config.use_database:
            db = cls.setup.config.get_database_connection_pool()
            if db is not None:
                for obj in cls.created_objects:
                    db.video.delete_one({"id": obj.id})
                print("Cleaned up test database.")

    def test_a_create_video(self):
        video_data = VideoEntity(
            external_id=str(uuid4()),
            email_user=self.email,
            video_input=f"./media/mercedez.mp4",
            frame_amount=10,
        )
        video = self.use_cases.create_video(video_data)
        self.created_objects.append(video)
        self.assertIsNotNone(video)
        self.assertEqual(video.email_user, video_data.email_user)
        self.assertEqual(video.is_processed, False)
        self.assertTrue(hasattr(video, "id"))

    def test_get_video(self):
        video_data = VideoEntity(email_user=self.email)
        fetched_video = self.use_cases.filter_videos(
            {"email_user": video_data.email_user}
        )
        self.assertIsNotNone(fetched_video)

    def test_list_videos(self):
        videos = self.use_cases.list_videos()
        self.assertIsInstance(videos, list)

    def test_process_video(self):
        video = self.use_cases.filter_videos_to_process({"email_user": self.email})
        if isinstance(video, list) and len(video) > 0:
            video = video[0]
        processed_video = self.use_cases.process_video(video)
        self.assertIsNotNone(processed_video)
        self.assertEqual(processed_video.id, video.id)
        self.assertTrue(processed_video.is_processed)
