from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


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


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('mentor', 'Mentor'),
    )

    email = models.EmailField(_("email address"), blank=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"), blank=True)
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"), blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='writer')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    objects = UserManager()

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.full_name

