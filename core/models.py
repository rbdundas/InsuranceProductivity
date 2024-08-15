from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from localflavor.us.models import USStateField


class User(AbstractUser):
    objects = UserManager()


class Role(models.Model):
    Name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.Name


class Account(models.Model):
    Name = models.CharField(max_length=120)
    NAICSCode = models.CharField(max_length=12, blank=True, null=True)
    Type = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.Name


class AccountTokens(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Token = models.CharField(max_length=120)


class AccountUser(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def list_record(self):
        return f"{self.User} : {self.Account}"

    def __str__(self):
        return self.list_record


class Address(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Type = models.CharField(max_length=20, null=True, blank=True)
    Street1 = models.CharField(max_length=120)
    Street2 = models.CharField(max_length=120, null=True, blank=True)
    City = models.CharField(max_length=120)
    State = models.CharField(USStateField)
    ZipCode = models.CharField(max_length=10)

    @property
    def list_record(self):
        return f"{self.Type} : {self.Account}"

    def __str__(self):
        return self.list_record


class CorporateContact(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Category = models.CharField(max_length=30, null=True, blank=True)
    Description = models.CharField(max_length=120, null=True, blank=True)
    Type = models.CharField(max_length=30, null=True, blank=True)
    Name = models.CharField(max_length=120, null=True, blank=True)
    EmailAddress = models.CharField(max_length=120, null=True, blank=True)
    Title = models.CharField(max_length=60, null=True, blank=True)
    PhoneNumber = models.CharField(max_length=30, null=True, blank=True)

    @property
    def list_record(self):
        return f"{self.Category} : {self.Description} : {self.Title}"

    def __str__(self):
        return self.list_record


class EpicSDKConfiguration(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Token = models.CharField(max_length=120)
    Database = models.CharField(max_length=20)
    Host = models.CharField(max_length=120)
    EndpointURL = models.CharField(max_length=200)
    UserCode = models.CharField(max_length=12)
    DatalakeInstance = models.CharField(max_length=25, null=True, blank=True)
    GoogleProjectID = models.CharField(max_length=25, null=True, blank=True)
    GoogleJSONFilename = models.CharField(max_length=60, null=True, blank=True)
    GoogleJSONFile = models.TextField(null=True, blank=True)
    Active = models.BooleanField(default=False)

    @property
    def list_record(self):
        return "%s: %s" % (self.Database, self.Host)

    def __str__(self):
        return self.list_record


class ClientType(models.Model):
    Type = models.CharField(max_length=30, null=True, blank=True)
    Category = models.CharField(max_length=30, null=True, blank=True)
    Subcategory = models.CharField(max_length=30, null=True, blank=True)


class IdentificationType(models.Model):
    Type = models.CharField(max_length=30, null=True, blank=True)
    Category = models.CharField(max_length=30, null=True, blank=True)


class IdentificationNumber(models.Model):
    Type = models.ForeignKey(IdentificationType, on_delete=models.CASCADE)
    Number = models.CharField(max_length=30, null=True, blank=True)


class Client(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Type = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    Name = models.CharField(max_length=120)
    IdentificationNumber = models.ForeignKey(IdentificationNumber, on_delete=models.CASCADE, null=True, blank=True)



