from django.db import models

from epic_crm.users.models import User


class Client(models.Model):

    name = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=300, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    salesperson = models.ForeignKey(to=User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    default=None,
                                    related_name='client_assigned')

    def __str__(self):
        return f"Client [ {self.pk} - {self.name} ]"
