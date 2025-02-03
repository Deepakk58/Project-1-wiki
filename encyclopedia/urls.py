from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.loadEntry, name="loadEntry"),
    path("wiki", views.index, name="wiki"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("newEntry", views.newEntry, name="newEntry")
]
