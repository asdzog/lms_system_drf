from django.contrib import admin
from courses.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'course_description', 'owner')
    list_filter = ('course_name', 'owner',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson_name', 'lesson_description', 'video_url', 'course', 'owner')
    list_filter = ('lesson_name', 'course', 'owner')
