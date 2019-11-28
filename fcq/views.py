import operator
import re
import copy
from functools import reduce

from django.db.models import Q
from django.db.models.functions import Lower, Substr
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import serializers

from classes.models import Department, Class
from fcq.models import Professor, FCQ

from .forms import SearchForm
from .serializers import ProfessorSerializer

# Create your views here.


def fcq_search(request):
    ctx = {}
    ctx["form"] = SearchForm()
    return render(request, "fcq/fcq_search.html", ctx)


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


def view_professor(request, professor_id):
    ctx = {}
    professor_id = int(professor_id)
    # take advantage of relation for these queries!! :)
    professor_obj = get_object_or_404(Professor, id=professor_id)
    professorID = professor_obj.id
    ctx["professor_id"] = professor_obj.id
    ctx["firstName"] = professor_obj.firstName
    ctx["lastName"] = professor_obj.lastName

    fcq = FCQ.objects.filter(professor_id=professorID)
    ctx["numClasses"] = len(fcq)

    subjects = fcq.order_by().values_list('course__course_subject').distinct()
    subjectList = [subjects[i][0] for i in range(len(subjects))]
    subjectFcq = []
    for i in subjectList:
        subjectFcq.append(fcq.filter(course__course_subject=i))
    ctx["subjectList"] = subjectList
    ctx["subjectFcq"] = subjectFcq
    return render(request, "fcq/professor_detail.html", ctx)
