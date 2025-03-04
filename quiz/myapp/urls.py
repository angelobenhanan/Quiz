from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("<int:tryout_id>", views.tryoutDetails, name="tryoutDetails"),
]
