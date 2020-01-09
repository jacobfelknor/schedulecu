from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import forms, views

app_name = "users"

urlpatterns = [
    path("login_redirect/", views.login_redirect, name="login_redirect"),
    path("signup/", views.UserSignUpView.as_view(), name="signup"),
    path("password/", forms.change_password, name="change_password"),
    path("<username>/view/", views.view_profile, name="view_profile"),
    path("<username>/settings/", views.view_settings, name="view_settings"),
    path("audit/", views.model_form_upload, name='model_form_upload'),
    path(
        "<username>/edit-profile/",
        views.EditUserAccountView.as_view(),
        name="edit_info",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
