from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime

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

    def post(self, *args, **kwargs):
        user = self.request.user
        print(self.request.data)
        course_id = int(self.request.data[0]["course_id"])

        course_item = get_object_or_404(Course, pk=course_id)

        if course_item:
            url_for_payment, session_id = services.create_stripe_session(course_item)

            data = {
                "user": user,
                "date": datetime.date.today(),
                "paid_course": course_item,
                "amount": course_item.price,
                "payment_method": "transfer_to_account",
            }
            payment = Payment.objects.create(**data)
            payment.save()
            message = (f'Success! Stripe sessiond ID is: {session_id}.'
                       f'URL for payment: {url_for_payment} ')
            return Response({"message": message})
        else:
            return Response({"message": 'Error! Wrong course.'})
