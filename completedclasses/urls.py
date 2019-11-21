from django.urls import path

from . import views

app_name = "completedclasses"

urlpatterns = [
    path("add_to_completed_classes/", views.add_to_completed_classes,
         name="add_to_completed_classes"),
    path(
        "remove_to_completed_classes/", views.remove_from_completed_classes, name="remove_from_completed_classes"
    ),
]
