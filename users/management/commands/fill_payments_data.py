from django.core.management import BaseCommand

from courses.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_to_fill = []

        for user in User.objects.all():
            payment_to_fill.append(Payment(user=user, lesson=Lesson.objects.get(pk=2),
                                           payment_amount=75_000, payment_method='cash'))
        for user in User.objects.all():
            payment_to_fill.append(Payment(user=user, course=Course.objects.get(pk=2),
                                           payment_amount=125_000, payment_method='transfer_to_account'))

        Payment.objects.bulk_create(payment_to_fill)
