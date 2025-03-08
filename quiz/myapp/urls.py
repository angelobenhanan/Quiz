from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("<int:tryoutId>", views.tryoutDetails, name = "tryoutDetails"),
    path("tryoutCreation", views.createTryout, name = "creation"),
    path("<int:tryoutId>/tryoutEditor", views.editTryout, name = "editor"),
    path("<int:tryoutId>/delete", views.deleteTryout, name = "delete"),
    path("searchByName/<name>", views.searchByName, name = "searchByName"),
    path("searchByCategory/<category>", views.searchByCategory, name = "searchByCategory"),
    path("searchByDate/<date>", views.searchByDate, name = "searchByDate"),
    path("<int:tryoutId>/questionCreation/<int:questionId>", views.createQuestion, name = "questionCreation"),
    path("<int:tryoutId>/questionEditor/<int:questionId>", views.editQuestion, name = "questionEditor"),
    path("<int:tryoutId>/questions", views.questionDetails, name = "questionDetails"),
    path("<int:tryoutId>/delete/<int:questionId>", views.deleteQuestion, name = "deleteQuestion"),
]
