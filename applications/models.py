from django.db import models
from core.models import Account


class Category(models.Model):
    Category = models.CharField(max_length=30)


class Type(models.TextChoices):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Type = models.CharField(max_length=120)


class Application(models.Model):
    Name = models.CharField(max_length=120)
    Version = models.CharField(max_length=10, default='0.0.1')
    Description = models.TextField(blank=True, null=True)
    Type = models.ForeignKey(Type, on_delete=models.CASCADE)


class AccountApplication(models.Model):
    pass


class Value(models.Model):
    pass


class Mapping(models.Model):
    pass


class MappingValues(models.Model):
    pass



