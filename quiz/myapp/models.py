from django.db import models

class Tryout(models.Model):
    tryoutName = models.CharField(max_length=100, editable=True)
    tryoutDesc = models.CharField(max_length=100, editable=True)
    tryoutNums = models.IntegerField(default=0, editable=True)
    tryoutCategory = models.CharField(max_length=100, editable=True)
    creationDate = models.CharField(max_length=100, editable=False)
    workedOn = models.BooleanField(default=False, editable=True)

    def __str__(self):
        return self.tryoutName
    
class Question(models.Model):
    tryout = models.ForeignKey(Tryout, on_delete = models.CASCADE)
    questionTxt = models.CharField(max_length=100, editable=True)
    questionNum = models.IntegerField(default=1, editable=True)
    answer = models.CharField(max_length=100, editable=True)

    def __str__(self):
        return self.questionTxt