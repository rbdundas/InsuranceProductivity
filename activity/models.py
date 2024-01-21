from django.utils import timezone
from django.db import models


class Activity(models.Model):
    AccountID = models.IntegerField(null=True, blank=True)
    AccountTypeCode = models.CharField(max_length=10, null=True, blank=True)
    ActivityCode = models.CharField(max_length=4, null=True, blank=True)
    ActivityID = models.IntegerField(null=True, blank=True)
    AgencyCode = models.CharField(max_length=4, null=True, blank=True)
    AssociatedToID = models.IntegerField(null=True, blank=True)
    AssociatedToType = models.CharField(max_length=30, null=True, blank=True)
    BranchCode = models.CharField(max_length=4, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Priority = models.CharField(max_length=10, null=True, blank=True)
    Timestamp = models.DateTimeField(default=timezone.now, null=True, blank=True)
    WhoOwnerCode = models.CharField(max_length=10, null=True, blank=True)
    CategoryID = models.IntegerField(null=True, blank=True)
    GeneralLedgerItemIDForAssociatedToID = models.IntegerField(null=True, blank=True)
    EnteredDate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    AttachmentsYesNo = models.BooleanField(null=True, blank=True)
    LastUpdatedDate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    AssociatedToGUID = models.CharField(max_length=60, null=True, blank=True)
    LineID = models.IntegerField(null=True, blank=True)
    SMS = models.BooleanField(null=True, blank=True)


class CloseDetailValue(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    ActualCost = models.IntegerField(null=True, blank=True)
    ActualTimeHours = models.IntegerField(null=True, blank=True)
    ActualTimeMinutes = models.IntegerField(null=True, blank=True)
    ClosedReason = models.CharField(max_length=30, null=True, blank=True)
    ClosedStatus = models.CharField(max_length=20, null=True, blank=True)
    IgnoreOpenTasks = models.BooleanField(null=True, blank=True)
    AverageCost = models.IntegerField(null=True, blank=True)
    AverageTimeHours = models.IntegerField(null=True, blank=True)
    AverageTimeMinutes = models.IntegerField(null=True, blank=True)
    Duration = models.IntegerField(null=True, blank=True)


class DetailValue(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    ContactName = models.CharField(max_length=60, null=True, blank=True)
    ContactNumberEmail = models.CharField(max_length=60, null=True, blank=True)
    ContactVia = models.CharField(max_length=10, null=True, blank=True)
    FollowUpEndDate = models.DateField(null=True, blank=True)
    FollowUpEndTime = models.TimeField(null=True, blank=True)
    FollowUpStartDate = models.DateField(auto_now_add=True, null=True, blank=True)
    FollowUpStartTime = models.TimeField(null=True, blank=True)
    IssuingCompanyLookupCode = models.CharField(max_length=10, null=True, blank=True)
    PremiumPayableLookupCode = models.CharField(max_length=10, null=True, blank=True)
    PremiumPayableTypeCode = models.CharField(max_length=10, null=True, blank=True)
    ReminderDate = models.DateField(null=True, blank=True)
    ReminderTime = models.TimeField(null=True, blank=True)
    ContactPhoneCountryCode = models.CharField(max_length=10, null=True, blank=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    AmountQualifier = models.CharField(max_length=10, null=True, blank=True)
    Update = models.CharField(max_length=10, null=True, blank=True)
    ContactID = models.IntegerField(null=True, blank=True)


class Notes(models.Model):
    DetailValue = models.ForeignKey(DetailValue, on_delete=models.CASCADE)


class StatusOption(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    OptionName = models.CharField(max_length=10, null=True, blank=True)
    Value = models.IntegerField(null=True, blank=True)


class Tasks(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


class TaskItem(models.Model):
    Tasks = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    Description = models.CharField(max_length=100, null=True, blank=True)
    DueDate = models.DateField(null=True, blank=True)
    DueTime = models.DateTimeField(null=True, blank=True)
    Flag = models.CharField(max_length=20, null=True, blank=True)
    Owner = models.CharField(max_length=12, null=True, blank=True)
    OwnerType = models.CharField(max_length=30, blank=True, null=True)
    StartDate = models.DateField(null=True, blank=True)
    StartTime = models.DateTimeField(null=True, blank=True)
    Status = models.CharField(max_length=30, null=True, blank=True)
    TaskID = models.IntegerField(null=True, blank=True)
    OrderNumber = models.CharField(max_length=30, null=True, blank=True)


class TaskNotes(models.Model):
    TaskItem = models.ForeignKey(TaskItem, on_delete=models.CASCADE)


class NoteItem(models.Model):
    Notes = models.ForeignKey(Notes, on_delete=models.CASCADE, null=True, blank=True)
    TaskNotes = models.ForeignKey(TaskNotes, on_delete=models.CASCADE, null=True, blank=True)
    AccessLevel = models.CharField(max_length=20, null=True, blank=True)
    Flag = models.CharField(max_length=20, null=True, blank=True)
    NoteID = models.IntegerField(null=True, blank=True)
    NoteText = models.TextField(max_length=1000, null=True, blank=True)


class ServicingContacts(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)


class AccountServicingContactItem(models.Model):
    ServicingContacts = models.ForeignKey(ServicingContacts, on_delete=models.CASCADE, null=True, blank=True)
    Code = models.CharField(max_length=10, null=True, blank=True)
    EmailAddress = models.CharField(max_length=120, null=True, blank=True)
    Extension = models.CharField(max_length=4, null=True, blank=True)
    Name = models.CharField(max_length=120, null=True, blank=True)
    ServicingRole = models.CharField(max_length=30, null=True, blank=True)


class WhoOwnerOption(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    OptionName = models.CharField(max_length=20, null=True, blank=True)
    Value = models.CharField(max_length=20, null=True, blank=True)


class IndioSubmissionValue(models.Model):
    Activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    CarrierSubmissionID = models.IntegerField(null=True, blank=True)
    SubmissionID = models.IntegerField(null=True, blank=True)


class ActivityType(models.Model):
    ActivityCode = models.CharField(max_length=4)
    Description = models.CharField(max_length=120, null=True, blank=True)
    Category = models.CharField(max_length=120, null=True, blank=True)
    PriorityCode = models.CharField(max_length=1, null=True, blank=True)
    Active = models.BooleanField(null=True, blank=True)
    IsClientVisible = models.BooleanField(null=True, blank=True)
    IsClientEditable = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Activity Types"

    @property
    def list_record(self):
        return f"{self.ActivityCode} : {self.Description}"

    def __str__(self):
        return self.list_record
