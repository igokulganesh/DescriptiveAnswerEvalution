from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..decorators import teacher_required
from ..models import Classroom, Enrollment, Test, Question, Answer


@login_required(login_url='login')
@teacher_required
def create_class(request):
	if request.method == "POST":
		name 	 = request.POST['name']
		desc 	 = request.POST.get('desc', '') 
		user 	 = request.user  
		code	 = request.POST['code']

		try:
			room = Classroom(owner=user, name=name, code=code, desc=desc)
			room.save()
			messages.success(request, '{} Class is Created'.format(room))
		except IntegrityError:
			messages.warning(request, "Code is already taken (Use Unique Code)")
			return redirect('create_class')

		return redirect('dashboard')

	return render(request, 'teachers/create_class.html')
	