from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..decorators import teacher_required
from ..models import Classroom, Enrollment, Test, Question, Answer
from ..forms import CreateTestForm


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
	

@login_required(login_url='login')
@teacher_required
def create_test(request, class_id):
	form = CreateTestForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form=CreateTestForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data.get('name')
			desc = form.cleaned_data.get('desc')
			posting_time = form.cleaned_data.get('posting_time')
			due_time = form.cleaned_data.get('due_time')
			
			belongs = get_object_or_404(Classroom, belongs=class_id)

			test = Test(belongs=belongs, name=name, desc=desc, posting_time=posting_time, due_time=due_time)
			test.save() 

			return view_class(request, class_id)
		else: 
			messages.error(request, form.errors)

	return render(request, 'teachers/create_test.html', {'form': form})


@login_required(login_url='login')
@teacher_required
def create_Qn(request, test_id):
	pass 