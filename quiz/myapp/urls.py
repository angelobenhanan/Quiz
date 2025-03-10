from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.home, name = "home"),
    path("<int:tryoutId>", views.tryoutDetails, name = "tryoutDetails"),
    path("tryoutCreation", views.createTryout, name = "creation"),
    path("<int:tryoutId>/tryoutEditor", views.editTryout, name = "editor"),
    path("<int:tryoutId>/delete", views.deleteTryout, name = "delete"),
    path("searchByName/<name>", views.searchByName, name = "searchByName"),
    path("searchByCategory/<category>", views.searchByCategory, name = "searchByCategory"),
    path("searchByDate/<date>", views.searchByDate, name = "searchByDate"),
    path("<int:tryoutId>/questionCreationTF/<int:questionId>", views.createQuestionTF, name = "questionCreationTF"),
    path("<int:tryoutId>/questionCreationMC/<int:questionId>", views.createQuestionMC, name = "questionCreationMC"),
    path("<int:tryoutId>/questionCreationEssay/<int:questionId>", views.createQuestionEssay, name = "questionCreationEssay"),
    path("<int:tryoutId>/questionEditorTF/<int:questionId>", views.editQuestionTF, name = "questionEditorTF"),
    path("<int:tryoutId>/questionEditorMC/<int:questionId>", views.editQuestionMC, name = "questionEditorMC"),
    path("<int:tryoutId>/questionEditorEssay/<int:questionId>", views.editQuestionEssay, name = "questionEditorEssay"),
    path("<int:tryoutId>/questions", views.questionDetails, name = "questionDetails"),
    path("<int:tryoutId>/delete/<int:questionId>", views.deleteQuestion, name = "deleteQuestion"),
    path("<int:tryoutId>/doTryout", views.doTryout, name = "doTryout"),
    
    #swagger
    path("/tryoutAPIview", TryoutListAPIView.as_view(), name="tryoutOperations"),
    path("/questionAPIview", QuestionListAPIView.as_view(), name="questionOperations"),
]