import operator
import re
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from fcq.models import Teacher
from rest_framework import serializers
from .serializers import TeacherSerializer


# Create your views here.

def fcq_search(request):
    return render(request, "fcq/fcq_search.html")

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