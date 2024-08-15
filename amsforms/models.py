from django.db import models
from core.models import Account


class AMSType(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    AMS = models.CharField(max_length=255, choices=(('EPIC', 'Epic'), ))

    def __str__(self):
        return f"{self.AMS} | {self.Account}"


class FormDefinition(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    FormTitle = models.CharField(max_length=255)
    Description = models.TextField()

    def __str__(self):
        return f"{self.FormTitle} - {self.Account.Name}"


class AMSObjectType(models.Model):
    AMSType = models.ForeignKey(AMSType, on_delete=models.CASCADE)
    FormDefinition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE)
    AMSObjectType = models.CharField(max_length=255, choices=(('Activity', 'Activity'), ('Client', 'Client'),
                                                              ('Opportunity', 'Opportunity'), ('Policy', 'Policy'), ))

    def __str__(self):
        return f"{self.AMSType} | {self.FormDefinition} | {self.AMSObjectType}"


class AMSObjectValue(models.Model):
    AMSObjectType = models.ForeignKey(AMSObjectType, on_delete=models.CASCADE)
    AMSField = models.CharField(max_length=255)
    Required = models.BooleanField()

    def __str__(self):
        return f"{self.AMSObjectType} | {self.AMSField} | {self.Required}"


class AMSObjectValueDefault(models.Model):
    AMSObjectType = models.ForeignKey(AMSObjectType, on_delete=models.CASCADE)
    AMSObjectValue = models.ForeignKey(AMSObjectValue, on_delete=models.CASCADE)
    DefaultValue = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.AMSObjectValue} | {self.DefaultValue}"


class FormToAMSValueMapping(models.Model):
    AMSObjectType = models.ForeignKey(AMSObjectType, on_delete=models.CASCADE)
    AMSObjectValue = models.ForeignKey(AMSObjectValue, on_delete=models.CASCADE)
    FormField = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.AMSObjectType} | {self.AMSObjectValue} | {self.FormField}"


class JotformParameters(models.Model):
    FormDefinition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE)
    FormID = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.FormDefinition} | {self.FormID} | {self.Username}"

    class Meta:
        verbose_name_plural = "Jotform Parameters"
        verbose_name = "Jotform Parameters"


class CognitoParameters(models.Model):
    FormDefinition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE)
    FormID = models.CharField(max_length=255)
    InternalName = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.FormDefinition} | {self.FormID} | InternalName | {self.InternalName}"

    class Meta:
        verbose_name_plural = "Cognito Parameters"
        verbose_name = "Cognito Parameters"
