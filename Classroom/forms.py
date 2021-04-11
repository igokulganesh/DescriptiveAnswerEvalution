from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Classroom, Enrollment, Test, Question, Answer
from django.contrib.auth.models import User

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
        fields=( 'name', 'desc', 'posting_time', 'due_time' )
        widgets={
        'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Test Name'}),
        'desc':forms.Textarea(attrs={'class':'form-control','placeholder':'Description','row':'2'}),
        }

    due_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
