from django.db import models

# Create your models here.
class Tryout(models.Model):
    tryoutName = models.CharField(max_length=100)
    tryoutDescp = models.CharField(max_length=100)
    tryoutNums = models.IntegerField()

    def __str__(self):
        return self.tryoutName