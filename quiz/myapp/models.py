from django.db import models

# Create your models here.
class TryoutList(models.Model):
    tryoutName = models.CharField(max_length=100)
    tryoutDescp = models.CharField(max_length=100)
    tryoutNums = models.IntegerField()