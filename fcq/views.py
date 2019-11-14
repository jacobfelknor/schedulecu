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
        return render(request, "fcq/fcq_display.html")

def fcq_search_ajax(request):
    if request.method == "GET":
        get = request.GET.get
    else:
        get = request.POST.get
    name = get("name", "")
    subject = get("subject", "")
    course = get("course", "")
    teachers = Teacher.objects.all()
    if name != '' or subject != '':
        if name != '':
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
            teachers = teachers.filter(name_query)
        if subject != '':
            if course != '':
                subject += ' ' + course
            teachers = teachers.filter(courseList__icontains=subject)
    teachers = teachers.order_by("lastName")
    response = TeacherSerializer(teachers, many=True)
    return JsonResponse(response.data, safe=False)

class TeacherView(DetailView):
    model = Teacher