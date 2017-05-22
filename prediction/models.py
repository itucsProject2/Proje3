from django.db import models
from django.template.defaultfilters import default
from datetime import date

# Create your models here.
class Data(models.Model):
    date = models.DateField()
    location = models.CharField(max_length = 30)
    product = models.CharField(max_length = 30)
    amount = models.IntegerField()