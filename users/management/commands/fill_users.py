from django.core.management.base import BaseCommand
from users.models import User, UserRoles


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Создаем список пользователей с разными ролями
        users_data = [
            {'email': 'user1@mail.net', 'phone': '+79201234567', 'role': UserRoles.MEMBER},
            {'email': 'user2@mail.net', 'phone': '+79309876543', 'role': UserRoles.MEMBER},
            {'email': 'moder1@mail.net', 'phone': '+79501234567', 'role': UserRoles.MODERATOR},
            {'email': 'moder2@mail.net', 'phone': '+79609876543', 'role': UserRoles.MODERATOR},
        ]

        passwords = ['userpass1', 'userpass2', 'moderpass1', 'moderpass2']

        users_with_passwords = []
        for idx, data in enumerate(users_data):
            user = User(
                email=data['email'],
                phone=data['phone'],
                role=data['role']
            )
            user.set_password(passwords[idx])
            users_with_passwords.append(user)

        User.objects.bulk_create(users_with_passwords)
