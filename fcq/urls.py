from django.urls import path

from . import views

app_name = "fcq"

urlpatterns = [
    path("fcq_search/", views.fcq_search, name="fcq_search"),
    path("fcq_search_ajax/", views.fcq_search_ajax, name="fcq_search_ajax"),
    path("view/<professor_id>/", views.view_professor, name="view"),
]

