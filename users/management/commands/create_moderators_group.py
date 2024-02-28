from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import Lesson, Course


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        lesson_content_type = ContentType.objects.get_for_model(Lesson)
        course_content_type = ContentType.objects.get_for_model(Course)

        lesson_view_permissions = Permission.objects.filter(content_type=lesson_content_type,
                                                            codename__startswith='view_')
        course_view_permissions = Permission.objects.filter(content_type=course_content_type,
                                                            codename__startswith='view_')

        lesson_change_permissions = Permission.objects.filter(content_type=lesson_content_type,
                                                              codename__startswith='change_')
        course_change_permissions = Permission.objects.filter(content_type=course_content_type,
                                                              codename__startswith='change_')

        moderator_permissions = lesson_view_permissions | course_view_permissions | lesson_change_permissions | course_change_permissions
        moderators_group.permissions.set(moderator_permissions)
