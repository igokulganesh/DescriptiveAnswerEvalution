from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Classroom, Enrollment, Test, Question, Answer
from django.contrib.auth.models import User
import datetime

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save()
        user.is_staff = True
        user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save()
        user.is_staff = False
        user.save()
        return user

class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields=( 'name', 'desc', 'start_time', 'end_time' )
        widgets={
        'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Test Name'}),
        'desc':forms.Textarea(attrs={ 'rows': 5, 'class':'form-control','placeholder':'Description'}),
        'start_time': forms.DateTimeInput(attrs={'type':'datetime-local','placeholder':'Assign Test At','class': 'form-control'},format='%Y-%m-%dT%H:%M'),
        'end_time': forms.DateTimeInput(attrs={'type':'datetime-local','placeholder':'Due Time', 'class': 'form-control'},format='%Y-%m-%dT%H:%M'),
        }
        labels={
            'start_time': 'Start Time',
            'end_time': 'End Time',
        }
