from django.urls import path

from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter

from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDeleteAPIView

app_name = CoursesConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')


urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lessons/', LessonListAPIView.as_view(), name='list_lesson'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='get_lesson'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete_lesson'),

    path('courses/<int:course_id>/subscribe/', SubscriptionCreateAPIView.as_view(), name='subscribe'),
    path('courses/<int:course_id>/unsubscribe/', SubscriptionDeleteAPIView.as_view(), name='unsubscribe'),

    path('courses/<int:pk>/course_detail/', CourseViewSet.as_view({'get': 'course_detail'}), name='course-detail'),

] + router.urls
