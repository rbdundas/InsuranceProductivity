from django.db import models
from activity.models import ActivityType
from core.models import Account


class JotformConfiguration(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    FormTitle = models.CharField(max_length=120)
    FormID = models.CharField(max_length=120)
    FieldAccountID = models.CharField(max_length=60, null=True, blank=True)
    AccountID = models.CharField(max_length=60, null=True, blank=True)
    FieldAssociatedToID = models.CharField(max_length=60, null=True, blank=True)
    AssociatedToID = models.CharField(max_length=60, null=True, blank=True)
    ActivityType = models.ForeignKey(ActivityType, on_delete=models.DO_NOTHING, null=True, blank=True)
    OwnerType = models.CharField(max_length=30, null=True, blank=True)
    OwnerCode = models.CharField(max_length=30, null=True, blank=True)
    Priority = models.CharField(max_length=10, null=True, blank=True)
    AccountTypeCode = models.CharField(max_length=4, blank=True, null=True)
    AssociatedToType = models.CharField(max_length=20, blank=True, null=True)

    @property
    def list_record(self):
        return f"{self.FormTitle} : {self.ActivityType}"

    def __str__(self):
        return self.list_record
