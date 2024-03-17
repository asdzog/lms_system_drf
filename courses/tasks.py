from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from courses.models import Subscription, Course


@shared_task
def send_course_update_notify(course: Course):
    """ Send email to user when the course is updated """

    subscriptions = Subscription.objects.all().filter(course=course)
    users = [subscription.user for subscription in subscriptions]
    for user in users:
        send_mail(
            subject="Обновление материалов курса",
            message=f"Материалы курса {course.course_name} были обновлены.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
