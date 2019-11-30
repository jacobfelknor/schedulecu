import operator
import re
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from classes.models import Class, Department, Section
from fcq.models import FCQ

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
            (Q(course_title__icontains=x) | Q(course_subject__icontains=x))
            for x in keyword
        ),
    )
    department = get("department")
    if department:
        department_obj = Department.objects.filter(code__iexact=department).first()
        if not department_obj:
            # return no results if department is not found
            return JsonResponse({})
        query = Q(department=department_obj) & keyword_query
    else:
        query = keyword_query
    # only show classes with sections
    classes = [
        x
        for x in Class.objects.filter(query).order_by("course_subject")
        if x.has_sections
    ]
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
    # only add to schedule functionality if user is logged in
    if request.user.is_authenticated and not ctx["generic_view"]:
        ctx["in_schedule"] = current_section.in_schedule(request.user)
        ctx["schedule"] = request.user.schedule.classes.all().order_by("start_time")



    # get number of semesters taught
    fcqs = FCQ.objects.filter(course=parent_class)
    yearList = fcqs.order_by().values_list("year").distinct()
    numSemesters = 0
    for i in range(len(yearList)):
        numSemesters += len(fcqs.filter(year=yearList[i][0]).order_by().values_list("semester").distinct())
    ctx["numSem"] = numSemesters

    #get avg course rating
    ratings = fcqs.order_by().values_list("courseRating")
    lenRat = len(ratings)
    sumRatings = 0
    for i in range(lenRat):
        sumRatings += ratings[i][0]
    avgCourse = round(sumRatings/lenRat,2)
    ctx["avgCourse"] = avgCourse

    #get avg course challenge
    challenge = fcqs.order_by().values_list("challenge")
    lenChal = len(challenge)
    sumChall = 0
    for i in range(lenChal):
        sumChall += challenge[i][0]
    avgChall = round(sumChall/lenChal,2)
    ctx["avgChall"] = avgChall



    return render(request, "classes/class_detail.html", ctx)
