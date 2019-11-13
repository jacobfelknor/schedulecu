import operator
import re
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.db.models.functions import Substr, Lower

from fcq.models import Teacher
from rest_framework import serializers
from .serializers import TeacherSerializer


# Create your views here.

def fcq_search(request):
    return render(request, "fcq/fcq_search.html")

def fcq_display(request):
    if request.method == "GET":
        get = request.GET.get
    else:
        get = request.POST.get
    name = get("name", "")
    department = get("department", "")
    subject = get("subject", "")
    course = get("course", "")
    name = re.split("\W", name)
    name_query = reduce(
        operator.and_,
        (
            (
                Q(firstName__icontains=x)
                | Q(lastName__icontains=x)
            )
            for x in name
        ),
    )
    course_query = reduce(operator.and_,(Q(courseList__contains=[x]) for x in course))
    subject_query = reduce(operator.and_, (Q(courseList__contains=[x]) for x in subject))
    query = course_query & subject_query
    teachers = Teacher.objects.filter(query)
    print(teachers)
    #keyword = re.split("\W", keyword)
    #keyword_query = reduce(
    #     operator.and_,
    #     (
    #         (
    #             Q(name__icontains=x)
    #         )
    #         for x in keyword
    #     ),
    # )
    # department = get("mainDepartment", "")

    # query = Q(mainDepartment__contains=department) & keyword_query

    # teachers = Teacher.objects.filter(query).order_by("name")
    #response = TeacherSerializer(teachers, many=True)



    return render(request, "fcq/fcq_display.html")

def fcq_search_ajax(request):
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
                Q(name__icontains=x)
            )
            for x in keyword
        ),
    )
    department = get("mainDepartment", "")

    query = Q(mainDepartment__contains=department) & keyword_query

    teachers = Teacher.objects.filter(query).order_by("name")
    response = TeacherSerializer(teachers, many=True)
    return JsonResponse(response.data, safe=False)

class TeacherView(DetailView):
    model = Teacher