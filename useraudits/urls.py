from django.urls import path

from . import views

app_name = "useraudits"

urlpatterns = [
    path("add_user_audit/", views.add_user_audit, name="add_user_audit"),
    path("remove_user_audit/", views.remove_user_audit, name="remove_user_audit"),
]
