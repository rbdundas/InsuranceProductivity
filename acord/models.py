from django.db import models


class AddressType(models.Model):
    Type = models.CharField(max_length=30)


class Address(models.Model):
    Type = models.ForeignKey(AddressType, on_delete=models.CASCADE)
    Address1 = models.CharField(max_length=240)
    Address2 = models.CharField(max_length=240)
    City = models.CharField(max_length=240)
    State = models.CharField(max_length=240)
    Zip = models.CharField(max_length=240)


class AgencyInformation(models.Model):
    Name = models.CharField(max_length=240)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE)
    ContactName = models.CharField(max_length=120)
    ContactPhone = models.CharField(max_length=30)
    ContactEmail = models.CharField(max_length=240)
    Code = models.CharField(max_length=4, blank=True, null=True)
    SubCode = models.CharField(max_length=4, blank=True, null=True)


class CarrierInformation(models.Model):
    Name = models.CharField(max_length=240)
    NAIC = models.CharField(max_length=4, blank=True, null=True)


class TransactionStatus(models.Model):
    Status = models.CharField(max_length=30)


class LinesOfBusiness(models.Model):
    Name = models.CharField(max_length=240, blank=True, null=True)


class Attachment(models.Model):
    Name = models.CharField(max_length=240)
    Description = models.CharField(max_length=240)


class Application(models.Model):
    AgencyInformation = models.ForeignKey(AgencyInformation, on_delete=models.CASCADE)
    Date = models.DateField()
    CarrierInformation = models.ForeignKey(CarrierInformation, on_delete=models.CASCADE)
    PolicyNumber = models.CharField(max_length=60, null=True, blank=True)
    Underwriter = models.CharField(max_length=60, null=True, blank=True)
    UnderwriterOffice = models.CharField(max_length=60, null=True, blank=True)
    AgencyCustomerID = models.CharField(max_length=60, null=True, blank=True)
    TransactionStatus = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE, null=True, blank=True)
    BindTimestamp = models.DateTimeField(null=True, blank=True)
    LinesOfBusiness = models.ManyToManyField(LinesOfBusiness, blank=True)
    Attachments = models.ManyToManyField(Attachment, blank=True)





