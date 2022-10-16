from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy

from recipes.validators import (validate_forbidden_username,
                                validate_unique_case_insensitive_email,
                                validate_unique_case_insensitive_username)


class User(AbstractUser):
    username = models.CharField(
        gettext_lazy('username'),
        max_length=150,
        unique=True,
        help_text=gettext_lazy('Required. 150 characters or fewer. '
                               'Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(),
                    validate_forbidden_username,
                    validate_unique_case_insensitive_username],
        error_messages={
            'unique':
                gettext_lazy('A user with that username already exists.'),
        },
    )
    email = models.EmailField(
        gettext_lazy('email address'),
        blank=False,
        null=False,
        unique=True,
        validators=[validate_unique_case_insensitive_email],
        error_messages={
            'unique':
                'Пользователь с таким адресом электронной почты '
                'уже существует.'
        }
    )
    first_name = models.CharField(
        gettext_lazy('first name'),
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        gettext_lazy('last name'),
        max_length=150,
        blank=False
    )
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='following'
    )
    subscriber = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'subscriber'),
                name='unique_follow_model'
            )
        ]
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
