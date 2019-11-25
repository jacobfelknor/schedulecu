from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from classes.models import Class, Section
from audit.models import Prerequisite
from .models import Schedule
from completedclasses.models import CompletedClasses
from django.contrib import messages

# Create your views here.


def add_to_schedule(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    schedule = request.user.schedule
    completed_classes = request.user.completed
    add_section_id = get("section_id")
    class_id = get("class_id")
    add_section = get_object_or_404(Section, pk=add_section_id)
    add_class = get_object_or_404(Class, pk=class_id)

    prereqs = Prerequisite.objects.filter(classes=add_class).filter(audit=None)

    prereq_failures = []
    coreq_failures = []
    for prereq in prereqs:
        # Needs to check possibleClasses not classes
        # in_completed = CompletedClasses.objects.filter(
        #    classes=pre_class.classes, user=request.user).exists()
        possibleClasses = [x for x in prereq.possibleClasses.all()]
        in_completed = CompletedClasses.objects.filter(
            classes__in=possibleClasses, user=request.user).exists()

        if prereq.corequisite:
            in_coreq = Schedule.objects.filter(
                classes__parent_class__in=possibleClasses, user=request.user).exists()
            if not in_completed and not in_coreq:
                coreq_failures += [prereq]
        else:
            if not in_completed:
                prereq_failures += [prereq]

    if len(prereq_failures) == 0 and len(coreq_failures) == 0:
        schedule.classes.add(add_section)
        messages.success(
            request,
            "{} {} has been successfully added to your schedule!".format(
                add_section.parent_class.department.code,
                add_section.parent_class.course_subject,
            ),
        )
    else:
        # INCOMPLETE MESSAGING. make this nicer
        messages.success(
            request,
            "To add this class, add the prerequisites " +
            str(list(set([y.department.code + str(y.course_subject) for x in prereq_failures for y in x.possibleClasses.all()]))) +
            "and the corequisites " +
            str(list(set([y.department.code +
                          str(y.course_subject) for x in coreq_failures for y in x.possibleClasses.all()]))),
            extra_tags="danger",
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
