import re
from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_pattern = r'^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+(\?\S*)?$'
        url = dict(value).get(self.field)
        if not re.match(youtube_pattern, url) is None:
            raise ValidationError('Недопустимая ссылка на сторонний ресурс')
