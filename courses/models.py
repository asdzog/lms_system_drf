from django.db import models
from django.conf import settings


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='название курса')
    course_description = models.TextField(verbose_name='описание курса')
    course_icon = models.ImageField(upload_to='courses/', **NULLABLE, verbose_name='превью')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    price = models.PositiveIntegerField(default=1000, verbose_name='цена')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name='название урока')
    lesson_description = models.TextField(verbose_name='описание урока')
    lesson_icon = models.ImageField(upload_to='courses/', **NULLABLE, verbose_name='превью')
    video_url = models.CharField(max_length=250, **NULLABLE, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                               related_name='lessons',
                               **NULLABLE, verbose_name='курс')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.user}: {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
