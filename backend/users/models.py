from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user', 'user'
        ADMIN = 'admin', 'admin'

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email')
    first_name = models.CharField(
        max_length=150,
        verbose_name='first_name')
    last_name = models.CharField(
        max_length=150,
        verbose_name='last_name')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username')
    role = models.CharField(
        max_length=30,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        verbose_name='role')

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь, который подписывается')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь, на которого подписываемся')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
