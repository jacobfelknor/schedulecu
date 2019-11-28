import operator
import re
import copy
from functools import reduce

from django.db.models import Q
from django.db.models.functions import Lower, Substr
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import serializers

from classes.models import Department, Class
from fcq.models import Professor, FCQ

from .forms import SearchForm
from .serializers import FcqSerializer, ProfessorSerializer

# Create your views here.


def fcq_search(request):
    ctx = {}
    ctx["form"] = SearchForm()
    return render(request, "fcq/fcq_search.html", ctx)


# this view is unused for now
def fcq_display(request):
    return render(request, "fcq/fcq_display.html")


def fcq_search_ajax(request):
    if request.method == "GET":
        get = request.GET.get
    else:
        get = request.POST.get

    results = FCQ.objects

    keyword = get("keyword", "")
    keyword = re.split("\W", keyword)
    fcq_obj = FCQ.objects.filter(reduce(
        operator.and_,
        (
            (
                Q(professor__firstName__icontains=x)
                | Q(professor__lastName__icontains=x)
            )
            for x in keyword
        ),
    ))  
    total = copy.copy(fcq_obj)
    department = get("department")
    if department:
        department_obj = Department.objects.filter(code__iexact=department).first()
        if not department_obj:
            # return no results if department is not found
            return JsonResponse({})
        else:
            fcq_obj = fcq_obj.filter(course__department__code=department)

    number = get("number")
    if number:
        number = int(number)
        print(type(number),number)
        fcq_obj = fcq_obj.filter(course__course_subject=number)
        
    profList = fcq_obj.order_by().values_list('professor').distinct()
    professors = Professor.objects.filter(id__in=profList).order_by("lastName")
    response = ProfessorSerializer(professors, many=True)
    return JsonResponse(response.data, safe=False)


class ProfessorView(DetailView):
    model = Professor
