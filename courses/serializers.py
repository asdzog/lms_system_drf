from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='course_name', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('course',)
