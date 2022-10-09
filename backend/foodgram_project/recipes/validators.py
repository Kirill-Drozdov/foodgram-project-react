from django.core.exceptions import ValidationError


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
