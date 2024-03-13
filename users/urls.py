from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, PaymentCreateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('create_user/', UserCreateAPIView.as_view(), name='create_user'),
    path('buy_course/', PaymentCreateAPIView.as_view(), name='buy_course'),

]
