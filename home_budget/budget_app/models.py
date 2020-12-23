from django.db import models
from datetime import date


class FamilyMember(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)


class MoneyTransfer(models.Model):
    date = models.DateField(default=date.today())
    owner = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
