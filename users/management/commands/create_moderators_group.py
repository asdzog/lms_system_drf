from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        content_type = ContentType.objects.get_for_model(User)
        permissions = Permission.objects.filter(content_type=content_type)

        moderators_permissions = []
        for permission in permissions:
            if permission.codename.startswith('change_') or permission.codename.startswith('view_'):
                moderators_permissions.append(permission)
        moderators_group.permissions.set(moderators_permissions)
