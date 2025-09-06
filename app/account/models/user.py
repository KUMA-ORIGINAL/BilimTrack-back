from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_("The Username field is required"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)


ROLE_ADMIN = "admin"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('mentor', 'Ментор'),
        ('scheduler', 'Составитель расписания'),
        (ROLE_ADMIN, 'Админ'),
    )

    email = models.EmailField(_("Адрес электронной почты"), blank=True)
    first_name = models.CharField(max_length=100, verbose_name=_("Имя"), blank=True)
    last_name = models.CharField(max_length=100, verbose_name=_("Фамилия"), blank=True)
    patronymic = models.CharField(
        max_length=100,
        verbose_name=_("Отчество"),
        blank=True,
        null=True  # если хотите разрешить NULL в БД
    )
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True)
    photo = ProcessedImageField(
        upload_to='user_photos/%Y/%m',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        verbose_name=_("Фотография")
    )
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name=_("Роль")
    )
    achievements_count = models.PositiveIntegerField(
        default=0,
        blank=True,
        verbose_name=_("Количество достижений")
    )
    points = models.PositiveIntegerField(
        default=0,
        blank=True,
        verbose_name=_("Баллы")
    )
    rating = models.PositiveIntegerField(
        default=0,
        blank=True,
        verbose_name=_("Рейтинг")
    )

    plain_password = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Пароль (открытый)',
        help_text='Если изменится пароль, то этот будет не действителен'
    )

    google_meet_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на Google Meet"
    )
    mentor_achievements = models.TextField(verbose_name='Достижения ментора', blank=True, null=True)

    instagram = models.URLField("Instagram", max_length=255, blank=True, null=True)
    telegram = models.URLField("Telegram", max_length=255, blank=True, null=True)
    whatsapp = models.URLField("Whatsapp", max_length=255, blank=True, null=True)
    facebook = models.URLField("Facebook", max_length=255, blank=True, null=True)

    skills = models.ManyToManyField(
        'Skill',
        related_name='users',
        verbose_name='Навыки',
        blank=True
    )
    tools = models.ManyToManyField(
        'Tool',
        related_name='users',
        blank=True,
        verbose_name=_("Инструменты")
    )

    achievements = models.ManyToManyField(
        'Achievement',
        related_name='users',
        blank=True,
        verbose_name=_("Достижения")
    )

    group = models.ForeignKey(
        'academics.Group',
        on_delete=models.CASCADE,
        related_name='users',
        blank=True,
        null=True,
        verbose_name=_("Группа")
    )
    organization = models.ForeignKey('academics.Organization', on_delete=models.CASCADE, verbose_name='Учебное заведение')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        indexes = [
            models.Index(fields=['role']),  # фильтр только по роли
            models.Index(fields=['organization']),  # фильтр только по организации
            models.Index(fields=['organization', 'role']),  # фильтр по организации + роли
        ]

    def __str__(self):
        return f'{self.username} - {self.full_name}'
