from django import forms
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .models import User


class UserSignUpForm(UserCreationForm):

    # success_url = reverse_lazy('accounts:view_account', kwargs={"test":"test"}) # broken
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name') 

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:view_profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

class UserAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone' ,'email') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_info = super(UserAccountForm, self).save(commit=False)
        # if user:
        #     user_profile.user = user
        user_info.save()
        return user_info