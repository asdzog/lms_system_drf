from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson, Subscription
from courses.paginators import CoursesPagination
from users.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CoursesPagination

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.request.user.groups.filter(name='moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action in ('create', ):
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ('list', 'retrieve', 'update', 'partial_update'):
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ('destroy', ):
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['get'])
    def course_detail(self, request, pk):
        course = self.get_object()
        subscribed = course.subscriptions.filter(
            user=request.user
        ).exists() if request.user.is_authenticated else False
        serializer = self.get_serializer(course)
        data = serializer.data
        data['subscribed'] = subscribed
        return Response(data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]  # for testing mode
    # permission_classes = [IsAuthenticated, ~IsModerator]  # for usual mode

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CoursesPagination

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if self.request.user.groups.filter(name='moderators').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]


class SubscriptionCreateAPIView(APIView):
    """Create subscription over course id"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, подписан ли пользователь на курс
        subscribed = Subscription.objects.filter(user=user, course=course).exists()

        if subscribed:
            # Если подписка у пользователя на этот курс есть - удаляем ее
            Subscription.objects.filter(user=user, course=course).delete()
            return Response({'message': f'Вы успешно отписались от курса {course.course_name}.'},
                            status=status.HTTP_200_OK)
        else:
            # Если подписки у пользователя на этот курс нет - создаем ее
            Subscription.objects.create(user=user, course=course)
            # Возвращаем ответ в API
            return Response({'message': f'Вы успешно подписались на курс {course.course_name}.'},
                            status=status.HTTP_201_CREATED)


class SubscriptionListAPIView(generics.ListAPIView):
    """Display list of user's subscriptions"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Subscription.objects.all()
        return queryset.filter(user=self.request.user)


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    """Delete user's subscription over its pk"""

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        user_id = self.request.user.pk

        subscription = Subscription.objects.get(course_id=course_id, user_id=user_id)

        if self.request.user == subscription.user:
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
