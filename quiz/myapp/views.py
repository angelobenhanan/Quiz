from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "Main.html")

def tryoutDetails(request):
    return render(request, "TryoutDetails.html")