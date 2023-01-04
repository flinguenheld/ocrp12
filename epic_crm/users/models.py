from django.db import models
from django.contrib.auth.models import User


class UserEpic(models.Model):

    class Roles(models.TextChoices):
        MANAGER = 'Manager'
        SALESPERSON = 'Salesperson'
        TECH_SUPPORT = 'Technical support'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=Roles.choices, max_length=50, default=Roles.MANAGER)

    # groups = 'bordel'
    # user_permissions = None
    # objects = UserManager()

    def save(self, *args, **kwargs):
        self.is_staff = self.role == UserEpic.Roles.MANAGER
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User [ {self.pk} - {self.role} ]"
