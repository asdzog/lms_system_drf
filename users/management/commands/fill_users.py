from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserRoles


class Command(BaseCommand):
    help = 'Create users with different roles'

    def handle(self, *args, **options):
        User = get_user_model()

        # Создаем список пользователей с разными ролями
        users_data = [
            {'username': 'user1', 'email': 'user1@mail.net', 'phone': '+79201234567', 'role': UserRoles.MEMBER},
            {'username': 'user2', 'email': 'user2@mail.net', 'phone': '+79309876543', 'role': UserRoles.MEMBER},
            {'username': 'moder1', 'email': 'moder1@mail.net', 'phone': '+79501234567', 'role': UserRoles.MODERATOR},
            {'username': 'moder2', 'email': 'moder2@mail.net', 'phone': '+78544386479', 'role': UserRoles.MODERATOR},
        ]

        passwords = ['userpass1', 'userpass2', 'moderpass1', 'moderpass2']

        for index, data in enumerate(users_data):
            user = User.objects.create(**data)
            password = passwords[index]
            user.set_password(password)
            user.save()
