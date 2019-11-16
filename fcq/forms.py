from ajax_select.fields import AutoCompleteField
from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Instructor Name"}),
        required=False,
    )
    department = AutoCompleteField(
        "major", label="", show_help_text=False, required=False
    )
