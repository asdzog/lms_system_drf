from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from courses.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='user@mail.net',
            password='test_psw',
            is_active=True
        )

        self.user.set_password(self.user.password)
        self.user.save()

        # self.client.force_authenticate(user=self.user)
        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

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
                        "lesson_name": self.lesson.lesson_name,
                        "lesson_description": self.lesson.lesson_description,
                        "lesson_icon": self.lesson.lesson_icon,
                        "video_url": self.lesson.video_url,
                        "course": self.course.course_name,
                        "owner": self.user.email
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
            'course': self.course,
            'owner': self.user
        }

        response = self.client.post(reverse('courses:create_lesson'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        response_lessons = self.client.get(
            reverse('courses:list_lesson')
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            response_lessons.json()['count']
        )

    def test_create_lesson_validation_error(self):
        """Error validation test"""

        data = {
            'lesson_name': 'test3',
            'lesson_description': self.lesson.lesson_description,
            'video': 'example.com'
        }
        response = self.client.post(
            reverse('courses:create_lesson'),
            data=data,
            user=self.user
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_update_lesson(self):
        """Test of updating a lesson"""
        new_description = 'updated_description'
        data = {
            'lesson_name': 'TestUpdate',
            'lesson_description': new_description,
            'video_url': self.lesson.video_url,
            'course': self.course.course_name,
            'owner': self.user.email
        }

        response = self.client.put(
            f'/lesson/update/{self.lesson.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        """Test of deleting a lesson"""

        response = self.client.delete(reverse('courses:delete_lesson',
                                              args=[self.lesson.pk])
                                      )
        print(response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

class SubscriptionAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='user@mail.net',
            password='test_psw',
            is_active=True,
        )

        self.user.set_password(self.user.password)
        self.user.save()

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.course = Course.objects.create(
            course_name='test_course',
            course_description='test_description',
            owner=self.user
        )

    def test_create_subscription(self):
        """Test of creating a subscription"""
        data = {
            "user": self.user.pk,
            "course": self.course.pk,
        }

        response = self.client.post(
            reverse('courses:subscribe'),
            data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete_subscription(self):
        """Test of deleting a subscription"""
        data = {
            "user": self.user.pk,
            "course": self.course.pk,
        }

        response = self.client.post(
            reverse('courses:subscribe'),
            data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

