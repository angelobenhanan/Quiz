from django.db import models

class Tryout(models.Model):
    tryoutName = models.CharField(max_length=100, editable=True)
    tryoutDesc = models.CharField(max_length=100, editable=True)
    tryoutNums = models.IntegerField(editable=True)
    tryoutCategory = models.CharField(max_length=100, editable=True)
    creationDate = models.DateField(max_length=100, default="", editable=False)
    workedOn = models.BooleanField(default=False, editable=True)

    def __str__(self):
        return self.tryoutName