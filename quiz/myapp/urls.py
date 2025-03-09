from django.urls import path, include
from django.contrib import admin
from myapp.swagger import schema_view
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from . import views
from myapp.views import *

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
    path("<int:tryoutId>/doTryout", views.doTryout, name = "doTryout"),
    
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path("schema_view", get_schema_view),
]