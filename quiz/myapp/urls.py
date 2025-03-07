from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("details/<int:tryout_id>", views.tryoutDetails, name = "tryoutDetails"),
    path("tryoutCreation", views.createTryout, name = "creation"),
    path("editor/<int:tryout_id>", views.editTryout, name = "editor"),
    path("delete/<int:tryout_id>", views.deleteTryout, name = "delete"),
    path("searchByName/<name>", views.searchByName, name = "searchByName"),
    path("searchByCategory/<category>", views.searchByCategory, name = "searchByCategory"),
]
