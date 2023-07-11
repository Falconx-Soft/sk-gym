from django import forms
from django.db import models
# from django.contrib.auth.models import User
from .models import User
     
class UserForm (forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['username', 'phone', 'email', 'password', 'profile_pic']


class MemberForm (forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model=User
        fields=['username', 'phone', 'email', 'blood_group', 'fee_amount','is_fee_paid', 'profile_pic', 'due_date']


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))