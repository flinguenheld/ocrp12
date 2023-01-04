from django.db import models

from epic_crm.users.models import UserEpic
from epic_crm.contracts.models import Contract


class Event(models.Model):

    name = models.CharField(max_length=150, unique=True)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    informations = models.CharField(max_length=500, blank=True)

    contract = models.OneToOneField(to=Contract,
                                    on_delete=models.CASCADE)

    technical_support = models.ForeignKey(to=UserEpic,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          default=None)

    def __str__(self):
        return f"Event [ {self.pk} - {self.name} - {self.date} - {self.contract} ]"
