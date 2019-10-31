from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

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
    department = get("department", "")

    query = Q(department__contains=department) & Q(course_title__icontains=keyword)

    classes = Class.objects.filter(query).order_by("course_subject")
    response = ClassSerializer(classes, many=True)
    return JsonResponse(response.data, safe=False)
