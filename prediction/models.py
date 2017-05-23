from django.db import models
from django.template.defaultfilters import default
from datetime import date

# Create your models here.
class Data(models.Model):
    tarih = models.DateField()
    magaza = models.CharField(max_length = 30)
    lokasyon = models.CharField(max_length = 30)
    kod = models.BigIntegerField()
    urunAdi = models.CharField(max_length = 30)
    anaGrup =  models.CharField(max_length = 30)
    altGrup =  models.CharField(max_length = 30)
    urunCesidi = models.CharField(max_length = 30)
    miktar = models.IntegerField()

class Date_Group(models.Model):
    tarih = models.DateField()
    kod = models.BigIntegerField()
    miktar = models.IntegerField()