from django.urls import path

from . import views

app_name = "classes"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("search_ajax/", views.search_ajax, name="search_ajax"),
    path("view/<pk>/", views.ClassView.as_view(), name="view"),
]

