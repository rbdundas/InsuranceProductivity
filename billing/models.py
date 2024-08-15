from django.db import models
from core.models import Account, User
from datetime import datetime


class EventType(models.Model):
    Type = models.CharField(max_length=30, null=True, blank=True)
    Category = models.CharField(max_length=30, choices=(('Service', 'Service'), ('Product', 'Product'), ('Consulting', 'Consulting')))


# Create your models here.
class BillingEvent(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Event = models.ForeignKey(EventType, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Description = models.TextField(null=True, blank=True)



