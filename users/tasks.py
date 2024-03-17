from celery import shared_task
from django.core.mail import send_mail

from users.models import User
from datetime import datetime, timedelta
from django.conf import settings


@shared_task
def check_users_activity():
    month_ago = datetime.now() - timedelta(days=30)
    users = User.objects.all()
    for user in users:
        if user.last_login < month_ago:
            user.is_active = False
            user.save()
            send_mail(
                subject="Удаление учетной записи",
                message=f"Привет! Учетная запись {user.email} была удалена из-за отсутствия активности",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
