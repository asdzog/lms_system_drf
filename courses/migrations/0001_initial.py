# Generated by Django 5.0.1 on 2024-01-30 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100, verbose_name='название курса')),
                ('course_description', models.TextField(verbose_name='описание курса')),
                ('course_icon', models.ImageField(blank=True, null=True, upload_to='courses/', verbose_name='превью')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=100, verbose_name='название урока')),
                ('lesson_description', models.TextField(verbose_name='описание урока')),
                ('lesson_icon', models.ImageField(blank=True, null=True, upload_to='courses/', verbose_name='превью')),
                ('video_url', models.CharField(blank=True, max_length=250, null=True, verbose_name='ссылка на видео')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course', verbose_name='курс')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]
