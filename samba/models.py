from django.db import models
from core.models import Account


class SambaSettings(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ClientID = models.CharField(max_length=120)
    ClientSecret = models.CharField(max_length=240)
    APIKey = models.CharField(max_length=240)
    URL = models.CharField(max_length=240)

