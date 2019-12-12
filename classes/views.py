import operator
import re
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from classes.models import Class, Department, Section
from audit.models import Prerequisite
from completedclasses.models import CompletedClasses
from schedules.models import Schedule
from fcq.models import FCQ

from .forms import SearchForm
from .serializers import SectionSerializer
from .serializers import ClassSerializer

# Create your views here.


def search(request):
    ctx = {}
    ctx["form"] = SearchForm()
    return render(request, "classes/search.html", ctx)


def search_ajax(request):
    if request.method == "GET":
        get = request.GET.get
    else:
        get = request.POST.get

    keyword = get("keyword", "")
    keyword = re.split("\W", keyword)
    sections = Section.objects.filter(
        reduce(
            operator.and_,
            (
                (
                    Q(professor__firstName__icontains=x)
                    | Q(professor__lastName__icontains=x)
                    | Q(parent_class__course_title__icontains=x)
                    | Q(parent_class__course_subject__icontains=x)
                )
                for x in keyword
            ),
        )
    )
    department = get("department")
    if department:
        sections = sections.filter(parent_class__department__code=department)
    # sections = sections.order_by(
    #     "parent_class__department__code", "parent_class__course_subject"
    # ).distinct("parent_class__department__code", "parent_class__course_subject")

    # mySQL does not support distinct(.....)
    sections = sections.order_by(
        "parent_class__department__code", "parent_class__course_subject"
    ).distinct()

    response = SectionSerializer(sections, many=True)
    return JsonResponse(response.data, safe=False)


def view_section(request, class_id, section_id):
    ctx = {}
    # take advantage of relation for these queries!! :)
    parent_class = get_object_or_404(Class, id=class_id)
    ctx["parent_class"] = parent_class
    if section_id != "all":
        current_section = get_object_or_404(Section, id=section_id)
        ctx["current_section"] = current_section
        ctx["generic_view"] = False
    else:
        ctx["generic_view"] = True
    lectures = parent_class.sections.filter(class_component="LEC")
    recitations = parent_class.sections.filter(class_component="REC")
    labs = parent_class.sections.filter(class_component="LAB")
    seminars = parent_class.sections.filter(class_component="SEM")
    other_query = (
        Q(class_component="SEM")
        | Q(class_component="LAB")
        | Q(class_component="REC")
        | Q(class_component="LEC")
    )
    other = parent_class.sections.exclude(other_query)
    ctx["lectures"] = lectures
    ctx["recitations"] = recitations
    ctx["labs"] = labs
    ctx["seminars"] = seminars
    ctx["other"] = other

    # Build prereq and coreq lists
    prereqs = Prerequisite.objects.filter(classes=parent_class).filter(audit=None)
    completed_prereqs = []
    incomplete_prereqs = []
    completed_coreqs = []
    incomplete_coreqs = []

    if request.user.is_authenticated:

        for prereq in prereqs:
            possibleClasses = [x for x in prereq.possibleClasses.all()]
            in_completed = CompletedClasses.objects.filter(
                classes__in=possibleClasses, user=request.user
            ).exists()

            if prereq.corequisite:
                in_coreq = Schedule.objects.filter(
                    classes__parent_class__in=possibleClasses, user=request.user
                ).exists()
                if not in_completed and not in_coreq:
                    incomplete_coreqs += [prereq]
                else:
                    completed_coreqs += [prereq]
            else:
                if not in_completed:
                    incomplete_prereqs += [prereq]
                else:
                    completed_prereqs += [prereq]

        if parent_class in request.user.completed.classes.all():
            ctx["in_completed"] = True

        if not ctx["generic_view"]:
            ctx["in_schedule"] = current_section.in_schedule(request.user)
        ctx["schedule"] = request.user.schedule.classes.all().order_by("start_time")
    else:
        for prereq in prereqs:
            if prereq.corequisite:
                incomplete_coreqs += [prereq]
            else:
                incomplete_prereqs += [prereq]

    ctx["completed_prereqs"] = completed_prereqs
    ctx["incomplete_prereqs"] = incomplete_prereqs
    ctx["completed_coreqs"] = completed_coreqs
    ctx["incomplete_coreqs"] = incomplete_coreqs

    # get number of semesters taught
    fcqs = FCQ.objects.filter(course=parent_class)
    yearList = fcqs.order_by().values_list("year").distinct()
    numSemesters = 0
    for i in range(len(yearList)):
        numSemesters += len(
            fcqs.filter(year=yearList[i][0])
            .order_by()
            .values_list("semester")
            .distinct()
        )
    ctx["numSem"] = numSemesters

    # get avg course rating
    ratings = fcqs.order_by().values_list("courseRating")
    lenRat = len(ratings)
    sumRatings = 0
    if lenRat > 0:
        for i in range(lenRat):
            sumRatings += ratings[i][0]
        avgCourse = round(sumRatings / lenRat, 2)
    else:
        avgCourse = "N/A"
    ctx["avgCourse"] = avgCourse

    # get avg course challenge
    challenge = fcqs.order_by().values_list("challenge")
    lenChal = len(challenge)
    sumChall = 0
    if lenChal > 0:
        for i in range(lenChal):
            sumChall += challenge[i][0]
        avgChall = round(sumChall / lenChal, 2)
    else:
        avgChall = "N/A"
    ctx["avgChall"] = avgChall

    return render(request, "classes/class_detail.html", ctx)
