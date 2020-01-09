from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from schedules.models import Schedule

from .forms import UserAccountForm, UserSignUpForm, DocumentForm
from .models import User, Document

# Create your views here.


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = ""
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home:home")


@login_required
def login_redirect(request):
    return redirect("accounts:account_list")


@login_required
def view_settings(request, username):
    if request.user.username != username:
        raise PermissionDenied()
    ctx = {}
    user = request.user
    if user.empty_fields():
        ctx["profile_complete"] = False
    else:
        ctx["profile_complete"] = True    
    return render(request, "users/view_settings.html", ctx)


@login_required
def view_profile(request, username):
    if request.user.username != username:
        raise PermissionDenied()
    ctx = {}
    user = request.user
    if user.empty_fields():
        ctx["profile_complete"] = False
    else:
        ctx["profile_complete"] = True
    ctx["schedule"] = request.user.schedule.classes.all().order_by("start_time")
    
    documents = Document.objects.all()
    ctx["documents"] = documents

    return render(request, "users/view_profile.html", ctx)


class EditUserAccountView(
    UpdateView
):  # Note that we are using UpdateView and not FormView
    model = User
    form_class = UserAccountForm
    template_name = "users/user_update.html"

    def get_object(self, *args, **kwargs):
        if self.request.user.username == self.kwargs["username"]:
            user = get_object_or_404(User, username=self.kwargs["username"])
        else:
            raise PermissionDenied()
        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["message"] = "Update Profile"
        return ctx

    # def get_success_url(self, *args, **kwargs):
    #     return reverse("accounts.views.view_account")


def model_form_upload(request):
    if request.method == 'POST':
        username = request.user.username
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:view_profile', username)
    else:
        form = DocumentForm()
    return render(request, 'users/model_form_upload.html', {
        'form': form
    })