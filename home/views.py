from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from users.models import User
from schedules.models import Schedule
from classes.models import Class

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        schedule = request.user.schedule.classes.all()
        context = {"schedule": schedule}
        return render(request, "home/home.html", context)

    return render(request, "home/home.html")

