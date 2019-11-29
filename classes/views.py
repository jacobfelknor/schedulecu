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

from .forms import SearchForm
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
    keyword_query = reduce(
        operator.and_,
        (
            (
                Q(course_title__icontains=x)
                # | Q(instructor_name__icontains=x)
                | Q(course_subject__icontains=x)
            )
            for x in keyword
        ),
    )
    department = get("department")
    if department:
        department_obj = Department.objects.filter(
            code__iexact=department).first()
        if not department_obj:
            # return no results if department is not found
            return JsonResponse({})
        query = Q(department=department_obj) & keyword_query
    else:
        query = keyword_query
    classes = Class.objects.filter(query).order_by("course_subject")
    response = ClassSerializer(classes, many=True)
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
    prereqs = Prerequisite.objects.filter(
        classes=parent_class).filter(audit=None)
    completed_prereqs = []
    incomplete_prereqs = []
    completed_coreqs = []
    incomplete_coreqs = []

    if request.user.is_authenticated:
        # complete = Prerequisite.objects.filter(
        #     classes=parent_class, corequisite=False, __possibleClasses__classes__in= CompletedClasses.objects.filter(
        #    classes__in=[y for x in prereqs.all() for y in x.possibleClasses.all()], user=request.user).
        #    )

        # All of user's completed classes that apply to these prereqs
        # Prerequisite.objects.filter(classes=parent_class, corequisite=False)
        # CompletedClasses.objects.filter(
        #     classes__in=[y for x in prereqs.all() for y in x.possibleClasses.all()], user=request.user)

        # All classes that apply
        # [x.classes.all() for x in CompletedClasses.objects.filter(classes__in=[y for x in prereqs.all() for y in x.possibleClasses.all()]).all()]

        for prereq in prereqs:
            possibleClasses = [x for x in prereq.possibleClasses.all()]
            in_completed = CompletedClasses.objects.filter(
                classes__in=possibleClasses, user=request.user).exists()

            if prereq.corequisite:
                in_coreq = Schedule.objects.filter(
                    classes__parent_class__in=possibleClasses, user=request.user).exists()
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
            # if self.object in self.request.user.schedule.classes.all():
            #     ctx["in_schedule"] = True
            ctx["in_schedule"] = current_section.in_schedule(request.user)
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
    # ctx["prereqs"] = {prereq: prereq.possibleClasses.all()
    #                  for prereq in prereqs}

    return render(request, "classes/class_detail.html", ctx)
