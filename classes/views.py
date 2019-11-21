import operator
import re
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from classes.models import Class, Department, Section

from .serializers import ClassSerializer
from .forms import SearchForm

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
                Q(parent_class__course_title__icontains=x)
                | Q(instructor_name__icontains=x)
                | Q(parent_class__course_subject__icontains=x)
            )
            for x in keyword
        ),
    )
    department = get("department")
    if department:
        department_obj = Department.objects.filter(code__iexact=department).first()
        if not department_obj:
            # return no results if department is not found
            return JsonResponse({})
        query = Q(parent_class__department=department_obj) & keyword_query
    else:
        query = keyword_query
    classes = Section.objects.filter(query).order_by("parent_class__course_subject")
    response = ClassSerializer(classes, many=True)
    return JsonResponse(response.data, safe=False)


class ClassView(DetailView):
    model = Section
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        related = Section.objects.filter(
            parent_class__course_subject=self.object.parent_class.course_subject,
            parent_class__department=self.object.parent_class.department,
        ).exclude(id=self.object.id)
        ctx["related"] = related
        # only add to schedule functionality if user is logged in
        if self.request.user.is_authenticated:
            if self.object in self.request.user.schedule.classes.all():
                ctx["in_schedule"] = True
        return ctx
