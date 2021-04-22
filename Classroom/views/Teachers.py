from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..decorators import teacher_required
from ..models import Classroom, Enrollment, Test, Question, Answer, testTaken
from ..forms import CreateTestForm, CreateQnForm, CreateClassForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User


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
def delete_class(request, class_id):
	room = get_object_or_404(Classroom, pk=class_id)
	messages.success(request, '{} is deleted'.format(room))
	room.delete()
	return redirect('dashboard')
	

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

	return render(request, 'teachers/create_test.html', {'form': form })

@login_required(login_url='login')
@teacher_required
def update_test(request, test_id):
	test = get_object_or_404(Test, pk=test_id)

	if request.method == "POST":
		form = CreateTestForm(request.POST, instance=test)

		if form.is_valid():
			form.save()
			messages.success(request, '{}  is Updated'.format(test))
			return redirect('view_test', test.id)
		else: 
			messages.error(request, form.errors)
	else:
		form = CreateTestForm(instance=test)
	return render(request, 'teachers/create_test.html', {'form': form, 'test' : test })

@login_required(login_url='login')
@teacher_required
def delete_test(request, test_id):
	test = get_object_or_404(Test, pk=test_id)
	room = test.belongs
	messages.success(request, '{} is deleted'.format(test))
	test.delete()
	return redirect('view_class', room.id)



@login_required(login_url='login')
@teacher_required
def view_test(request, test_id):
	qns = Question.objects.filter(test=test_id)
	test = get_object_or_404(Test, pk=test_id)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		qns = Question.objects.filter(test=test_id, qn_text__icontains=search)

	# paginator 
	paginator = Paginator(qns, 5)
	page = request.GET.get('page', 1)

	try:
		qns = paginator.page(page)
	except PageNotAnInteger:
		qns = paginator.page(1)
	except EmptyPage:
		qns = paginator.page(paginator.num_pages)

	return render(request, 'teachers/view_test.html', { 'qns' : qns, 'test' : test } )


@login_required(login_url='login')
@teacher_required
def students_work(request, test_id):
	qns = Question.objects.filter(test=test_id)
	test = get_object_or_404(Test, pk=test_id)
	student = Enrollment.objects.filter(room=test.belongs).values('student')
	attended_s = testTaken.objects.filter(test=test_id).values('student')
	missed_s = testTaken.objects.filter(~Q(student__id__in=student.all()), test=test_id).values('student')


	attended_s = User.objects.filter(pk__in=attended_s).values()
	missed_s = User.objects.filter(pk__in=missed_s).values()


	print(student)
	print(attended_s)

	values = {
		'qns' : qns, 
		'test': test,
		'student': student, 
		'attended_s':attended_s,
		'missed_s': missed_s,
	}

	return render(request, 'teachers/students_work.html', values )


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

	return render(request, 'teachers/create_qn.html', {'form': form})

@login_required(login_url='login')
@teacher_required
def update_qn(request, qn_id):
	qn = get_object_or_404(Question, pk=qn_id)

	if request.method == "POST":
		form = CreateQnForm(request.POST, instance=qn)

		if form.is_valid():
			form.save()
			messages.success(request, 'Question is Updated')
			return redirect('view_test', qn.test.id)
		else: 
			messages.error(request, form.errors)
	else:
		form = CreateQnForm(instance=qn)
	return render(request, 'teachers/create_qn.html', {'form': form, 'qn' : qn })

@login_required(login_url='login')
@teacher_required
def delete_qn(request, qn_id):
	qn = get_object_or_404(Question, pk=qn_id)
	test = qn.test
	messages.success(request, 'Question is deleted')
	qn.delete()
	return redirect('view_test', test.id)