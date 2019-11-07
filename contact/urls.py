from django.urls import path

from . import forms, views

app_name = "contact"

urlpatterns = [
    path("", views.ContactView.as_view(), name="contact")
]
