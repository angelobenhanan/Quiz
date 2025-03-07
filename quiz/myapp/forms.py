from django import forms
from django.core.exceptions import ValidationError
from .models import Tryout

tryoutCategory = [
    ("Math and Natural Science", "Math and Natural Science"),
    ("Social Science", "Social Science"),
    ("Random", "Random")
    ]

class TryoutCreationForm(forms.Form):
    tryoutName = forms.CharField(max_length= 100)
    tryoutDesc = forms.CharField(max_length= 100)
    tryoutCategory = forms.ChoiceField(widget=forms.RadioSelect, choices=tryoutCategory)

    def checkNameValid(self):
        name = self.cleaned_data["tryoutName"]
        takenNames = Tryout.objects.all()
        if (name not in takenNames) and (len(name) <= 100):
            return name
        else:
            return ValidationError("Invalid name!")
        
    def checkDescpValid(self):
        desc = self.cleaned_data["tryoutDesc"]
        if (len(desc) <= 100):
            return desc
        else:
            return ValidationError("Description must be at most 100 words long!")
    
    def checkCategoryValid(self):
        category = self.cleaned_data["tryoutCategory"]
        return category

class TryoutEditingForm(forms.Form):
    tryoutName = forms.CharField(max_length=100)
    tryoutDesc = forms.CharField(max_length=100)
    tryoutCategory = forms.ChoiceField(widget=forms.RadioSelect, choices=tryoutCategory)

    def checkNameValid(self):
        name = self.cleaned_data["tryoutName"]
        takenNames = Tryout.objects.all()
        if (name not in takenNames) and (len(name) <= 100):
            return name
        else:
            return ValidationError("Invalid name!")
        
    def checkDescpValid(self):
        desc = self.cleaned_data("tryoutDesc")
        if (len(desc) <= 100):
            return desc
        else:
            return ValidationError("Description must be at most 100 words long!")
        
    def checkCategoryValid(self):
        category = self.cleaned_data["tryoutCategory"]
        return category