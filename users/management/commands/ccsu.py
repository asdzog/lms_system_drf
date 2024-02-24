from django.core.management import BaseCommand
from users.models import User
from dotenv import load_dotenv
from django.conf import settings
import os


load_dotenv(settings.BASE_DIR / '.env')


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('ADM_EMAIL'),
            first_name='admin',
            last_name='DB_admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password(os.getenv('ADM_PSW'))
        user.save()
