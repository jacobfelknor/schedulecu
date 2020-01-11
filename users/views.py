from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from useraudits.management.commands.AddUserAudit import addEntries, removeEntries

from schedules.models import Schedule
from useraudits.models import UserAuditEntry

from .forms import UserAccountForm, UserSignUpForm, DocumentForm
from .models import User, Document

import PyPDF2

# Create your views here.


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = ""
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home:home")


@login_required
def login_redirect(request):
    return redirect("accounts:account_list")


@login_required
def view_settings(request, username):
    if request.user.username != username:
        raise PermissionDenied()
    ctx = {}
    user = request.user
    if user.empty_fields():
        ctx["profile_complete"] = False
    else:
        ctx["profile_complete"] = True    
    return render(request, "users/view_settings.html", ctx)


@login_required
def view_profile(request, username):
    if request.user.username != username:
        raise PermissionDenied()
    
    ctx = {}
    user = request.user
    ctx["schedule"] = request.user.schedule.classes.all().order_by("start_time")
    
    if UserAuditEntry.has_audit(user):
        audit = UserAuditEntry.objects.filter(user=user)
        auditList = UserAuditEntry.get_audit(user)
        ctx["audit"] = auditList
        department_obj = (
            audit.order_by().values_list("course__department__name").distinct()
        )
        departments = [x[0] for x in department_obj]
        deps = [["department", "count"]]
        for dep in departments:
            count = len(audit.filter(course__department__name=dep))
            holder = [dep, count]
            deps.append(holder)
        ctx["pieData"] = deps
    
    return render(request, "users/view_profile.html", ctx)


class EditUserAccountView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = User
    form_class = UserAccountForm
    template_name = "users/user_update.html"

    def get_object(self, *args, **kwargs):
        if self.request.user.username == self.kwargs["username"]:
            user = get_object_or_404(User, username=self.kwargs["username"])
        else:
            raise PermissionDenied()
        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["message"] = "Update Profile"
        return ctx

    # def get_success_url(self, *args, **kwargs):
    #     return reverse("accounts.views.view_account")


#handles form uploads
@login_required
def model_form_upload(request):
    if request.method == 'POST':
        username = request.user.username
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            auditObject = form.save()
            if not confirmAudit(auditObject):
                form = DocumentForm()
            else:
                audit = readAudit(auditObject)
                user = request.user
                removeEntries(user)
                addEntries(audit, user)
                documents = Document.objects.all()
                for document in documents:
                    document.delete()
                return redirect('users:view_profile', username)
    else:
        form = DocumentForm()
    return render(request, 'users/model_form_upload.html', {
        'form': form
    })


#confirms that the uploaded pdf is an official audit of CU
def confirmAudit(auditObject):
    audit = PyPDF2.PdfFileReader(auditObject.document)
    numPages = audit.numPages
    offset = len(str(numPages))
    test = 'THE FAMILY EDUCATIONAL RIGHTS AND PRIVACY ACT (FERPA) OF1974 SET FORTH REQUIREMENTS REGARDING THE PRIVACY OFSTUDENT RECORDS. THESE REQUIREMENTS GOVERN WHO THESERECORDS MAY BE RELEASED TO, WHO CAN ACCESS THESE RECORDS,AS WELL AS THE ACCURACY OF THE DATA IN THESE RECORDS.ALL FACULTY, STAFF AND STUDENTS SHOULD GUARD THEPROTECTION AND PRIVACY OF THIS DOCUMENT.THIS EVALUATION IS PROVIDED FOR ADVISEMENT; IT IS NOT ANOFFICIAL RECORD. PLEASE REPORT ANY ADDITIONS ORCORRECTIONS TO YOUR ACADEMIC ADVISOR.'
    page = audit.getPage(0)
    pageText = page.extractText()
    if test in pageText:
        return True
    else:
        return False


#get user's course history from audit
def readAudit(auditObject):
    audit = PyPDF2.PdfFileReader(auditObject.document)
    numPages = audit.numPages
    offset = len(str(numPages))
    course_data = []
    classes = False
    find = False

    #all classes a user has taken has been sectioned off. We just need to find the subj and course number
    #to store. We also need to look for 'TC' in the name of the course to see if the credit is a transfer
    #if it is a transfer, we need to find the equivalence of said course at CU.

    #Parse the pdf and grab the lines of text we're interested in (classes taken, gpa, major, minor, etc)
    for i in range(numPages):
        page = audit.getPage(i)
        pageText = page.extractText()
        text = pageText.split(' ')
        track = False
        for j in text:
            if j[offset:] == 'Coursework':
                track = True
            elif track:
                if j[:7] == 'History':
                    classes = True
                else:
                    track = False
            elif classes:
                if 'TermCourseCreditsGradeTitle' in j:
                    find = True
                    classes = False
            if find:
                if ('SP' in j or 'SU' in j or 'FA' in j) and ('NEED' not in j) and ('999TC' not in j):
                    course_data.append(j)

    #change the following substrings so we correctly parse lines of text:
    #Also, parse lines at 'TermCourseCreditsGradeTitle' if said substring exists
    for i in range(len(course_data)):
        if 'CSPB' in course_data[i]:
            course_data[i] = course_data[i].replace('CSPB','!!!!')
        if 'LDSP' in course_data[i]:
            course_data[i] = course_data[i].replace('LDSP','@@@@')
        if 'SPAN' in course_data[i]:
            course_data[i] = course_data[i].replace('SPAN','####')
        if 'SUST' in course_data[i]:
            course_data[i] = course_data[i].replace('SUST','$$$$')
        if 'FARR' in course_data[i]:
            course_data[i] = course_data[i].replace('FARR','&&&&')
        if 'TermCourseCreditsGradeTitle' in course_data[i]:
            course_data[i] = course_data[i].split('TermCourseCreditsGradeTitle')[1]

    #clean parsed data
    for i in range(len(course_data)):
        # print(course_data[i])
        if 'SP' in course_data[i]: #handle spring course
            holder = course_data[i].split('SP')
            if len(holder) == 3:
                course_data.append('SP' + holder[2])
            course_data[i] = 'SP' + holder[1]

        if 'SU' in course_data[i]: #handle summer course
            holder = course_data[i].split('SU')
            if len(holder) == 3:
                course_data.append('SU' + holder[2])
            course_data[i] = 'SU' + holder[1]

        if 'FA' in course_data[i]: #handle fall course
            holder = course_data[i].split('FA')
            if len(holder) == 3:
                course_data.append('FA' + holder[2])
            course_data[i] = 'FA' + holder[1]
            
    #finish parse and store all cleaned courses in array 
    course_history = []
    for i in range(len(course_data)):
        term = ''
        year = ''
        subject = ''
        courseNum = ''
        grade = ''
        holder = course_data[i][:18]

        if (holder[-1] != '-') and (holder[-1] != '+') and (holder[-1] != '*'):
            holder = holder[:-1]
        if holder[:2] == 'SP':
            term = 'Spring'
        elif holder[:2] == 'SU':
            term = 'Summer'
        elif holder[:2] == 'FA':
            term = 'Fall'

        holder = holder[2:]
        year = holder[:2]
        holder = holder[2:]
        subject = holder[:4]
        holder = holder[4:]
        courseNum = holder[:4]
        holder = holder[4:]
        credits = holder[:3]
        holder = holder[3:]
        holder = holder.replace('T', '')

        if holder[-1] == '*':
            grade = '*'
        elif (holder[-1] == '-') or (holder[-1] == '+'):
            grade = holder
        elif len(holder) == 1:
            grade = holder
        else:
            grade = holder[:-1]

        if subject == '!!!!':
            subject = 'CSPB'
        if subject == '@@@@':
            subject = 'LDSP'
        if subject == '####':
            subject = 'SPAN'
        if subject == '$$$$':
            subject = 'SUST'
        if subject == '&&&&':
            subject = 'FARR'

        holder = [term,year,subject,courseNum,grade,credits]
        course_history.append(holder)
    auditObject.document.close()
    return course_history


#delete all of user's stored audit data
@login_required
def reset_audit(request):
    user = request.user
    totalAudits = UserAuditEntry.objects.all()
    for entry in totalAudits:
        if entry.user == user:
            entry.delete()

    return redirect('users:view_profile', user.username)