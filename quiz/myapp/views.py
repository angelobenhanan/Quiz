from django.shortcuts import *
from .models import *

# Create your views here.
def home(request):
    tryoutList = Tryout.objects.all()
    return render(request, "Main.html", {"tryoutList": tryoutList})

def tryoutDetails(request, tryout_id):
    tryoutViewed = get_object_or_404(Tryout, pk=tryout_id)
    return render(request, "TryoutDetails.html", {"tryoutViewed": tryoutViewed})