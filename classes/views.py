import operator
import re
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from classes.models import Class

from .serializers import ClassSerializer

# Create your views here.


def search(request):
    return render(request, "classes/search.html")


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
                | Q(instructor_name__icontains=x)
                | Q(course_subject__icontains=x)
            )
            for x in keyword
        ),
    )
    department = get("department", "")

    query = Q(department__contains=department) & keyword_query

    classes = Class.objects.filter(query).order_by("course_subject")
    response = ClassSerializer(classes, many=True)
    return JsonResponse(response.data, safe=False)


class ClassView(DetailView):
    model = Class
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        related = Class.objects.filter(
            course_subject=self.object.course_subject, department=self.object.department
        ).exclude(id=self.object.id)
        ctx["related"] = related
        if self.object in self.request.user.schedule.classes.all():
            ctx["in_schedule"] = True
        return ctx
