from django.shortcuts import render
from django.views import generic
from django.views.generic import FormView
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .forms import ContactForm

# Create your views here.


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact/contact.html"

    success_url = reverse_lazy("home:home")

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = ""
        return super().get_context_data(**kwargs)

    # def get(self, request):
    #    return HttpResponse(reverse("contact"))

    def form_valid(self, form):
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["schedulecu@gmail.com"]
            if cc_myself:
                recipients.append(sender)

            messages.success(
                self.request,
                "Email successfully sent",
            )

            send_mail(subject, message, sender, recipients)
            # for now, redirect to home
            return super().form_valid(form)
