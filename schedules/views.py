from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from classes.models import Class, Section
from django.contrib import messages

# Create your views here.


def add_to_schedule(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    schedule = request.user.schedule
    add_section_id = get("section_id")
    class_id = get("class_id")
    add_section = get_object_or_404(Section, pk=add_section_id)
    schedule.classes.add(add_section)
    messages.success(
        request,
        "{} {} has been successfully added to your schedule!".format(
            add_section.parent_class.department.code,
            add_section.parent_class.course_subject,
        ),
    )
    return redirect("classes:view", class_id=class_id, section_id=add_section_id)


def remove_from_schedule(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    schedule = request.user.schedule
    remove_section_id = get("section_id")
    class_id = get("class_id")
    remove_section = get_object_or_404(Section, pk=remove_section_id)
    schedule.classes.remove(remove_section)
    messages.success(
        request,
        "{} {} has been successfully removed to your schedule!".format(
            remove_section.parent_class.department.code,
            remove_section.parent_class.course_subject,
        ),
        extra_tags="danger",
    )
    return redirect("classes:view", class_id=class_id, section_id=remove_section_id)
