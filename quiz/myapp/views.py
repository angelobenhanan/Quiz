from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.
def home(request):
    tryout = TryoutList.objects.all()
    return render(request, "Main.html", {"tryouts": tryout})

def tryoutDetails(request):
    return render(request, "TryoutDetails.html")