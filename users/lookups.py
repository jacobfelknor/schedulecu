from ajax_select import register, LookupChannel
from classes.models import Department

# TODO Populate majors with class code and degree from PDF


@register("major")
class MajorLookup(LookupChannel):

    model = Department

    def get_query(self, q, request):
        objects = self.model.objects.filter(code__icontains=q)
        majors = set([x.code for x in objects])
        return majors

    def format_match(self, item):
        return u"<span class='tag'>%s</span>" % item

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item

    def check_auth(self, request):
        return True
