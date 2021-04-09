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