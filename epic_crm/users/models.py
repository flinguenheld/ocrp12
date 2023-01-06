from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRole(models.Model):

    class Roles(models.TextChoices):
        MANAGER = 'Manager'
        SALESPERSON = 'Salesperson'
        TECH_SUPPORT = 'Technical support'

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='role_of')

    role = models.CharField(choices=Roles.choices,
                            max_length=50,
                            default=Roles.MANAGER)

    # groups = 'bordel'
    # user_permissions = None
    # objects = UserManager()

    def save(self, *args, **kwargs):

        self.user.is_staff = self.role == UserRole.Roles.MANAGER
        self.user.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Role [ {self.role} - {self.user} ]"


# --
# Use signals to automatically create and affect a role on new superuser
@receiver(post_save, sender=User)
def create_superuser(sender, instance, created, **kwargs):

    # if created and instance.is_superuser:
    if created and instance.is_superuser and not hasattr(instance, 'role_of'):
        UserRole.objects.create(user=instance, role=UserRole.Roles.MANAGER)
