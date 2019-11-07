from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False, label="CC Myself")
