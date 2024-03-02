from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson, Subscription
from users.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

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
            user=request.user).exists() if request.user.is_authenticated else False
        serializer = self.get_serializer(course)
        data = serializer.data
        data['subscribed'] = subscribed
        return Response(data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

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


class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        request = self.request
        user = request.user
        course_id = request.data.get('course_id')
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
