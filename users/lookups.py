from ajax_select import LookupChannel, register
from django.db.models import Q

from classes.models import Department

# TODO Populate majors with class code and degree from PDF


@register("major")
class MajorLookup(LookupChannel):

    model = Department

    def get_query(self, q, request):
        objects = self.model.objects.filter(Q(code__icontains=q) | Q(name__icontains=q))
        # majors = set([x.name for x in objects])
        return objects

    def format_match(self, obj):
        return "<span class='tag'>{}</span>".format(obj.name)

    def format_item_display(self, obj):
        return "<span class='tag'>{}</span>".format(obj.name)

    def get_result(self, obj):
        return obj.code

    def check_auth(self, request):
        return True
