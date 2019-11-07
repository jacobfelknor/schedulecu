from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from classes.models import Class
from django.contrib import messages

# Create your views here.


def add_to_schedule(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    schedule = request.user.schedule
    add_class_id = get("class_id")
    add_class = get_object_or_404(Class, pk=add_class_id)
    schedule.classes.add(add_class)
    messages.success(
        request,
        "{} {} has been successfully added to your schedule!".format(
            add_class.department, add_class.course_subject
        ),
    )
    return redirect("classes:view", pk=add_class_id)


def remove_from_schedule(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    schedule = request.user.schedule
    remove_class_id = get("class_id")
    remove_class = get_object_or_404(Class, pk=remove_class_id)
    schedule.classes.remove(remove_class)
    messages.success(
        request,
        "{} {} has been successfully removed to your schedule!".format(
            remove_class.department, remove_class.course_subject
        ),
        extra_tags="danger",
    )
    return redirect("classes:view", pk=remove_class_id)
