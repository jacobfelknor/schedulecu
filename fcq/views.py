import operator
import re
from functools import reduce

from django.db.models import Q
from django.db.models.functions import Lower, Substr
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import serializers

from classes.models import Department
from fcq.models import Teacher

from .forms import SearchForm
from .serializers import TeacherSerializer

# Create your views here.


def fcq_search(request):
    ctx = {}
    ctx["form"] = SearchForm()
    return render(request, "fcq/fcq_search.html", ctx)


def fcq_display(request):
    return render(request, "fcq/fcq_display.html")


# def fcq_search_ajax(request):
#     if request.method == "GET":
#         get = request.GET.get
#     else:
#         get = request.POST.get
#     name = get("name", "")
#     subject = get("subject", "")
#     course = get("course", "")
#     teachers = Teacher.objects.all()
#     if name != "" or subject != "":
#         if name != "":
#             name = re.split("\W", name)
#             name_query = reduce(
#                 operator.and_,
#                 ((Q(firstName__icontains=x) | Q(lastName__icontains=x)) for x in name),
#             )
#             teachers = teachers.filter(name_query)
#         if subject != "":
#             if course != "":
#                 subject += " " + course
#             teachers = teachers.filter(courseList__icontains=subject)
#     teachers = teachers.order_by("lastName")
#     response = TeacherSerializer(teachers, many=True)
#     return JsonResponse(response.data, safe=False)


def fcq_search_ajax(request):
    if request.method == "GET":
        get = request.GET.get
    else:
        get = request.POST.get

    keyword = get("keyword", "")
    keyword = re.split("\W", keyword)
    keyword_query = reduce(
        operator.and_,
        ((Q(firstName__icontains=x) | Q(lastName__icontains=x)) for x in keyword),
    )
    department = get("department")
    if department:
        department_obj = Department.objects.filter(code__iexact=department).first()
        if not department_obj:
            # return no results if department is not found
            return JsonResponse({})
        query = Q(mainDepartment=department_obj.code) & keyword_query
    else:
        query = keyword_query
    teachers = Teacher.objects.filter(query)
    response = TeacherSerializer(teachers, many=True)
    return JsonResponse(response.data, safe=False)


class TeacherView(DetailView):
    model = Teacher
