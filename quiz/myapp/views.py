from django.shortcuts import render, get_object_or_404
from .models import Tryout
from .forms import TryoutCreationForm, TryoutEditingForm
import datetime

# Create your views here.
def home(request):
    tryoutList = Tryout.objects.all()
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    return render(request, "Main.html", {"tryoutList": tryoutList})

def tryoutDetails(request, tryout_id):
    tryoutViewed = get_object_or_404(Tryout, pk = tryout_id)
    return render(request, "TryoutDetails.html", {"tryoutViewed": tryoutViewed})

def createTryout(request):
    if request.method == "POST":
        creationForm = TryoutCreationForm(request.POST, request.FILES)

        if (creationForm.is_valid()):
            name = creationForm.cleaned_data["tryoutName"]
            desc = creationForm.cleaned_data["tryoutDesc"]
            category = creationForm.data.get("tryoutCategory")
            date = datetime.date.today()
            newTryout = Tryout(tryoutName = name, tryoutNums = 0, tryoutDesc = desc, tryoutCategory = category, creationDate = date, workedOn = False)
            newTryout.save()
            return render(request, "TryoutDetails.html", {"tryoutViewed": newTryout})
    else:
        creationForm = TryoutCreationForm()
    return render(request, "TryoutCreation.html", {"creationForm": creationForm})

def editTryout(request, tryout_id):
    if request.method == "POST":
        editorForm = TryoutEditingForm(request.POST)
        tryoutChanged = get_object_or_404(Tryout, pk = tryout_id)

        if (editorForm.is_valid()):
            name = editorForm.cleaned_data["tryoutName"]
            desc = editorForm.cleaned_data["tryoutDesc"]
            category = editorForm.cleaned_data["tryoutCategory"]
            tryoutChanged.tryoutName = name
            tryoutChanged.tryoutDesc = desc
            tryoutChanged.tryoutCategory = category
            tryoutChanged.save()
            return render(request, "TryoutDetails.html", {"tryoutViewed": tryoutChanged})
    else:
        editorForm = TryoutCreationForm()
    return render(request, "TryoutEditor.html", {"editorForm": editorForm})

def deleteTryout(request, tryout_id):
    tryout = get_object_or_404(Tryout, pk = tryout_id)
    tryout.delete()
    tryoutList = Tryout.objects.all()
    return render(request, "Main.html", {"tryoutList": tryoutList})

def searchByName(request, name):
    tryoutList = Tryout.objects.all()
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": name})

def searchByCategory(request, category):
    tryoutList = Tryout.objects.all()
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    return render(request, "SearchByCategory.html", {"tryoutList": tryoutList, "category": category})