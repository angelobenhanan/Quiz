from django import forms
from django.core.exceptions import ValidationError
from .models import Tryout

tryoutCategory = [
    ("Math and Natural Science", "Math and Natural Science"),
    ("Social Science", "Social Science"),
    ("Random", "Random")
    ]

answers = [
    ("True", "True"), 
    ("False", "False")
    ]

class TryoutCreationForm(forms.Form):
    tryoutName = forms.CharField(max_length=100)
    tryoutDesc = forms.CharField(max_length=100)
    tryoutCategory = forms.ChoiceField(widget=forms.RadioSelect, choices=tryoutCategory)

    def checkNameValid(self):
        name = self.cleaned_data["tryoutName"]
        takenNames = Tryout.objects.all()
        if (name not in takenNames) and (len(name) <= 100):
            return name
        else:
            raise ValidationError("Invalid name!")
        
    def checkDescpValid(self):
        desc = self.cleaned_data["tryoutDesc"]
        if (len(desc) <= 100):
            return desc
        else:
            raise ValidationError("Description must be at most 100 words long!")
    
    def checkCategoryValid(self):
        category = self.cleaned_data["tryoutCategory"]
        return category

class TryoutEditingForm(forms.Form):
    tryoutName = forms.CharField(max_length=100)
    tryoutDesc = forms.CharField(max_length=100)
    tryoutCategory = forms.ChoiceField(widget=forms.RadioSelect, choices=tryoutCategory)

    #memastikan nama dan deskripsi sesuai
    def checkNameValid(self):
        name = self.cleaned_data["tryoutName"]
        takenNames = Tryout.objects.all()
        if (name not in takenNames) and (len(name) <= 100):
            return name
        else:
            raise ValidationError("Invalid name!")
        
    def checkDescpValid(self):
        desc = self.cleaned_data("tryoutDesc")
        if (len(desc) <= 100):
            return desc
        else:
            raise ValidationError("Description must be at most 100 words long!")
        
    def checkCategoryValid(self):
        category = self.cleaned_data["tryoutCategory"]
        return category
    
class QuestionCreationForm(forms.Form):
    questionTxt = forms.CharField(max_length= 100)
    answer = forms.CharField(max_length= 100)

    #memastikan soal dan pilihan jawaban sesuai
    def checkTxtValid(self):
        txt = self.cleaned_data["questionTxt"]
        if (len(txt) <= 100):
            return txt
        else:
            raise ValidationError("Description must be at most 100 words long!")
        
    def checkAnswer(self):
        answer = self.cleaned_data["answer"]
        return answer
    
class DoTryoutForm(forms.Form):
    answer = forms.ChoiceField(widget=forms.RadioSelect, choices=answers, label=("Answer: "), required=True)

    def checkAnswer(self):
        answer = self.cleaned_data["answer"]
        return answer
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length= 100)
    password = forms.CharField(max_length= 100)

    def checkUsername(self):
        username = self.cleaned_data["username"]
        return username
    
    def checkPassword(self):
        password = self.cleaned_data["password"]
        return password
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length= 100)
    password = forms.CharField(max_length= 100)

    def checkUsername(self):
        username = self.cleaned_data["username"]
        return username
    
    def checkPassword(self):
        password = self.cleaned_data["password"]
        return password