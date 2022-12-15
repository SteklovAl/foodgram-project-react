from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомизация модели пользователя:
    role - роль в системе
    confirmation_code - код подтверждения токена.
    """

    USER = 'user'
    ADMIN = 'admin'

    ROLE_USER = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        'E-mail',
        blank=False,
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    password = models.CharField(
        'Логин',
        max_length=150,
    )
    role = models.CharField(
        'Роль в системе',
        max_length=20,
        choices=ROLE_USER,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name',
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
