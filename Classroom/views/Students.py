from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ..decorators import student_required
from ..models import Classroom, Enrollment, Test, Question, Answer, testTaken


@login_required(login_url='login')
@student_required
def join_class(request):
	if request.method == "POST":
		code = request.POST['code']
		user = request.user 

		try:
			room = Classroom.objects.get(code=code)
		except Classroom.DoesNotExist:
			messages.warning(request, "There's no such Classroom")
			return redirect('join_class')

		if Enrollment.objects.filter(room=room, student=user).exists():
			messages.info(request, 'You Already Enrolled {}'.format(room))
		else: 
			Enrollment(room=room, student=user).save() 
			messages.success(request, '{} Class Enrolled'.format(room))

		return redirect('dashboard')

	return render(request, 'students/join_class.html')


@login_required(login_url='login')
@student_required
def attend_test(request, test_id):
	test = get_object_or_404(Test, id=test_id)

	if testTaken.objects.filter(test=test, student=request.user).exists():
		return redirect('review_test', test_id)

	qns = Question.objects.filter(test=test_id)
	return render(request, 'students/attend_test.html', { 'qns' : qns, 'test' : test } )


@login_required(login_url='login')
@student_required
def submit_test(request, test_id):
	qns = Question.objects.filter(test=test_id)
	test = get_object_or_404(Test, id=test_id)
	student = request.user 

	if testTaken.objects.filter(test=test, student=request.user).exists():
		return redirect('review_test', test_id)

	testTaken(test=test, student=student).save() 

	for q in qns:
		id = str(q.id)
		ans = request.POST[id] 
		Answer(student=student, question=q, answer_text=ans).save()

	return redirect('view_class', test.belongs.id)

@login_required(login_url='login')
@student_required
def review_test(request, test_id):
	test = get_object_or_404(Test, id=test_id)
	return redirect('dashboard')