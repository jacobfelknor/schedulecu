from django.urls import path

from . import views

app_name = "classes"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("search_ajax/", views.search_ajax, name="search_ajax"),
    # path("view/<class_id>/", views.view_class, name="view"),
    path("view/<class_id>/<section_id>", views.view_section, name="view"),
]

