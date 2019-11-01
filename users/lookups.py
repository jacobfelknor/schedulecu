from ajax_select import register, LookupChannel
from classes.models import Class

# TODO Populate majors with class code and degree from PDF 

@register("major")
class MajorLookup(LookupChannel):

    model = Class

    def get_query(self, q, request):
        objects = self.model.objects.filter(department__icontains=q)
        majors = set([x.department for x in objects])
        return majors

    def format_match(self, item):
        return u"<span class='tag'>%s</span>" % item

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item

    def check_auth(self, request):
        return True