# Generated by Django 4.2.7 on 2024-03-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_session_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='payment_session_id'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='payment_url'),
        ),
    ]