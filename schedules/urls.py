from django.urls import path

from . import views

app_name = "schedules"

urlpatterns = [
    path("add_to_schedule/", views.add_to_schedule, name="add_to_schedule"),
    path(
        "remove_to_schedule/", views.remove_from_schedule, name="remove_from_schedule"
    ),
]

