from django.db import models

from epic_crm.users.models import User
from epic_crm.clients.models import Client


class Contract(models.Model):

    signatory = models.ForeignKey(to=User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  related_name='Salesperson_signatory')
    date_signed = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(to=Client,
                               on_delete=models.CASCADE,
                               related_name='Client_signatory')
    date_created = models.DateTimeField(auto_now_add=True,
                                        editable=False)
    amount = models.FloatField(default=0.0)

    @property
    def signed(self):
        return self.date_signed is not None

    def __str__(self):
        return f"Contract [ {self.pk} - {self.client} - {self.date_signed} ]"
