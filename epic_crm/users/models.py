from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser):

    class Roles(models.TextChoices):
        MANAGER = _('Manager')
        SALESPERSON = _('Salesperson')
        TECH_SUPPORT = _('Technical support')

    username = None
    email = models.EmailField(_('email address'), unique=True)

    role = models.CharField(choices=Roles.choices, max_length=50, default=Roles.MANAGER)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.is_staff = self.role == User.Roles.MANAGER
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User [ {self.pk} - {self.email} - {self.role} ]"
