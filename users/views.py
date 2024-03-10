from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, serializers
from rest_framework.permissions import IsAuthenticated

from courses import services
from courses.models import Course
from users.models import Payment
from users.permissions import IsModerator, IsOwner
from users.serializers import PaymentSerializer, UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsModerator | IsOwner]
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("date",)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = Course.objects.get(pk=course_id)
        user = self.request.user

        if Payment.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError('Платеж уже произведен')
        else:
            serializer.save(
                user=user,
                course=course,
                payment_amount=course.price * 100,
                payment_method='перевод'
            )
