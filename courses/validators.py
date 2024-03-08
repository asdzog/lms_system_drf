from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)
        if not url:
            raise ValidationError('Не указана ссылка на урок')
        elif 'youtube.com' not in url.lower() and 'youtu.be' not in url.lower():
            raise ValidationError('Указана недопустимая ссылка на сторонний ресурс')
