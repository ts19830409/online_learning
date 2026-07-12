from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    """Проверяет, что ссылка ведёт на youtube.com"""
    if 'youtube.com' not in value.lower():
        raise ValidationError('Ссылка должна вести на youtube.com')