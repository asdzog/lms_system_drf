from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson, NULLABLE


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    email_verified = models.BooleanField(default=False, verbose_name='email подтвержден')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer_to_account', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='обучающийся')
    date = models.DateField(verbose_name="дата оплаты")
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный курс")
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный урок")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name="способ оплаты")

    def __str__(self):
        return f'{self.user}: {self.amount} ({self.date})'

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
