from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "home/home.html")

