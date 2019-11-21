from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from classes.models import Class
from django.contrib import messages


# Create your views here.
def add_to_completed_classes(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    completed_classes = request.user.completed
    add_class_id = get("class_id")
    add_class = get_object_or_404(Class, pk=add_class_id)
    completed_classes.classes.add(add_class)
    messages.success(
        request,
        "{} {} has been successfully added to your completed classes!".format(
            add_class.department.code, add_class.course_subject
        ),
    )
    return redirect("classes:view", pk=add_class_id)


def remove_from_completed_classes(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    completed_classes = request.user.completed
    remove_class_id = get("class_id")
    remove_class = get_object_or_404(Class, pk=remove_class_id)
    completed_classes.classes.remove(remove_class)
    messages.success(
        request,
        "{} {} has been successfully removed from your completed classes!".format(
            remove_class.department.code, remove_class.course_subject
        ),
        extra_tags="danger",
    )
    return redirect("classes:view", pk=remove_class_id)
