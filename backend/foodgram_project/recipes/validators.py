from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_amount(value):
    if value <= 0:
        raise ValidationError(
            'Значение поля "Количество" должно быть положительным!'
        )
    return value


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            ('Значение поля "Время приготовления"'
             ' должно быть не меньше 1 минуты!')
        )
    return value


def validate_forbidden_username(value):
    """Проверяет, что имя пользователя не является «me»."""
    if 'me' == value.lower():
        msg = f'Нельзя создать пользователя с именем «{value}».'
        raise ValidationError(msg)

    return value


def validate_unique_case_insensitive_username(value):
    """Проверяет, что username пользователя уникально."""
    user_model = get_user_model()
    if user_model.objects.filter(username__iexact=value).exists():
        msg = gettext_lazy('A user with that username already exists.')
        raise ValidationError(msg)
    return value


def validate_unique_case_insensitive_email(value):
    """Проверяет, что email пользователя уникален."""
    user_model = get_user_model()
    if user_model.objects.filter(email__iexact=value).exists():
        msg = 'Пользователь с таким адресом электронной почты уже существует.'
        raise ValidationError(msg)
    return value


def validate_unique_case_insensitive_first_name(value):
    """Проверяет, что first_name пользователя уникален."""
    user_model = get_user_model()
    if user_model.objects.filter(first_name__iexact=value).exists():
        msg = 'Пользователь с таким именем уже существует.'
        raise ValidationError(msg)
    return value


def validate_unique_case_insensitive_last_name(value):
    """Проверяет, что last_name пользователя уникален."""
    user_model = get_user_model()
    if user_model.objects.filter(last_name__iexact=value).exists():
        msg = 'Пользователь с такой фамилией уже существует.'
        raise ValidationError(msg)
    return value
