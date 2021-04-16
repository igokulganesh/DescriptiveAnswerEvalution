from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..decorators import teacher_required
from ..models import Classroom, Enrollment, Test, Question, Answer
from ..forms import CreateTestForm, CreateQnForm, CreateClassForm
from datetime import datetime


@login_required(login_url='login')
@teacher_required
def create_class(request):
	form = CreateClassForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form = CreateClassForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data.get('name')
			desc = form.cleaned_data.get('desc')
			code = form.cleaned_data.get('code')
			user = request.user 
			room = Classroom(owner=user, name=name, code=code, desc=desc)
			room.save()
			messages.success(request, '{} Class is Created'.format(room))
			return redirect('dashboard')
		else:
			messages.error(request, form.errors)
	return render(request, 'teachers/create_class.html', {'form': form})

@login_required(login_url='login')
@teacher_required
def update_class(request, class_id):
	room = get_object_or_404(Classroom, pk=class_id)
	if request.method == "POST":
		form = CreateClassForm(request.POST, instance=room)

		if form.is_valid():
			form.save()
			messages.success(request, '{} Class is Updated'.format(room))
			return redirect('view_class', class_id)
		else:
			messages.error(request, form.errors)
	else:
		form = CreateClassForm(instance=room)
	return render(request, 'teachers/create_class.html', {'form': form, 'room':room})
	

@login_required(login_url='login')
@teacher_required
def create_test(request, class_id):
	form = CreateTestForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form=CreateTestForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data.get('name')
			desc = form.cleaned_data.get('desc')
			start_time = form.cleaned_data.get('start_time')
			end_time = form.cleaned_data.get('end_time')
			
			belongs = get_object_or_404(Classroom, id=class_id)

			test = Test(belongs=belongs, name=name, desc=desc, start_time=start_time, end_time=end_time)
			test.save()

			return redirect('view_class', class_id)
		else: 
			messages.error(request, form.errors)

	return render(request, 'teachers/create_test.html', {'form': form, 'class_id' : class_id })

@login_required(login_url='login')
@teacher_required
def view_test(request, test_id):
	qns = Question.objects.filter(test=test_id)
	return render(request, 'teachers/view_test.html', { 'qns' : qns, 'test_id' : test_id } )


@login_required(login_url='login')
@teacher_required
def create_qn(request, test_id):
	form = CreateQnForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form = CreateQnForm(request.POST)

		if form.is_valid():
			text = form.cleaned_data.get('qn_text')
			key = form.cleaned_data.get('key')
			max_score = form.cleaned_data.get('max_score')
			
			test = get_object_or_404(Test, id=test_id)

			qn = Question(test=test, qn_text=text, key=key, max_score=max_score)
			qn.save()

			return redirect('view_test', test_id)
		else: 
			messages.error(request, form.errors)

	return render(request, 'teachers/create_qn.html', {'form': form, 'test_id' : test_id })
