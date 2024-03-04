from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from courses.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='user@mail.net',
            password='test_psw'
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            course_name='test_course',
            course_description='test_description',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            lesson_name='test_create_lesson',
            lesson_description='test_description',
            video_url="youtube.com/test_1",
            course=self.course,
            owner=self.user
        )

    def test_get_list(self):
        """Test of getting lessons list"""

        response = self.client.get(
            reverse('courses:list_lesson')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),

            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "lesson_name": "test_create_lesson",
                        "lesson_description": "test_description",
                        "lesson_icon": None,
                        "video_url": "youtube.com/test_1",
                        "course": self.course.id,
                        "owner": self.user.id
                    }
                ]
            }
        )

    def test_create_lesson(self):
        """Test of creating a lesson"""
        data = {
            'lesson_name': 'test_create_lesson',
            'lesson_description': 'test_description',
            'video_url': 'youtube.com/test_1',
            'course': self.course.id,
            'owner': self.user.id
        }

        response = self.client.post(reverse('courses:create_lesson'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "lesson_name": self.lesson.lesson_name,
                "lesson_description": self.lesson.lesson_description,
                "lesson_icon": None,
                "video_url": self.lesson.video_url,
                "course": self.course.id,
                "owner": self.user.id
                }
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_update_lesson(self):
        """Test of updating a lesson"""
        new_description = 'updated_description'
        data = {
            'lesson_name': 'TestUpdate',
            'lesson_description': new_description,
            'video_url': self.lesson.video_url,
            'course': self.course.id,
            'owner': self.user.id
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            f'/lesson/update/{self.lesson.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
