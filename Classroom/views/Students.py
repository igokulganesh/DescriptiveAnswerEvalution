from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ..decorators import student_required
from ..models import Classroom, Enrollment, Test, Question, Answer, testTaken
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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

	tt = testTaken(test=test, student=student, actual_score=0, ml_score=0)
	tt.save()

	for q in qns:
		id = str(q.id)
		ans = request.POST[id] 
		ans = Answer(student=student, question=q, answer_text=ans)
		ans.save()
		tt.actual_score += ans.actual_score
		tt.ml_score += ans.ml_score

	tt.save()

	return redirect('view_class', test.belongs.id)

@login_required(login_url='login')
@student_required
def review_test(request, test_id):
	test = get_object_or_404(Test, id=test_id)
	qns = Question.objects.filter(test=test_id)
	student = request.user 
	ans = []
	tot = 0
	act = 0  
	for i in range(len(qns)) :
		d = {} 
		d['qns'] = qns[i] 
		d['ans'] = get_object_or_404(Answer, student=student, question=qns[i]) # Answer.objects.filter(student=student, question=qns[i]) 
		ans.append(d)
		act += d['ans'].actual_score  
		tot = qns[i].max_score 

	mark = "{} / {}".format(act, tot)
	return render(request, 'students/review_test.html', { 'test' : test, 'ans' : ans, 'mark' : mark })


@login_required(login_url='login')
@student_required
def assigned_test(request, class_id):
	tests = Test.objects.filter(belongs=class_id)
	taken = list(testTaken.objects.filter(~Q(student=request.user), test__in=tests).values("test"))

	d = []
	for t in taken: 
		d.append( t['test'] )
	tests = Test.objects.filter(pk__in=d, belongs=class_id, start_time__lt=datetime.datetime.now(), end_time__gt=datetime.datetime.now()).order_by('-create_time')

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		tests = Test.objects.filter(belongs=class_id, name__icontains=search).order_by('-create_time')


	# paginator 
	paginator = Paginator(tests, 5)
	page = request.GET.get('page', 1)

	try:
		tests = paginator.page(page)
	except PageNotAnInteger:
		tests = paginator.page(1)
	except EmptyPage:
		tests = paginator.page(paginator.num_pages)

	for t in tests:
		t.status = "Assigned"
		
	room = get_object_or_404(Classroom, id=class_id)
	return render(request, 'classroom/view_class.html', {'tests' : tests, 'room' : room } )


@login_required(login_url='login')
@student_required
def missing_test(request, class_id):
	tests = Test.objects.filter(belongs=class_id)
	taken = list(testTaken.objects.filter(~Q(student=request.user), test__in=tests).values("test"))

	d = []
	for t in taken: 
		d.append( t['test'] )
	tests = Test.objects.filter(pk__in=d, belongs=class_id)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		tests = Test.objects.filter(belongs=class_id, name__icontains=search).order_by('-create_time')


	# paginator 
	paginator = Paginator(tests, 5)
	page = request.GET.get('page', 1)

	try:
		tests = paginator.page(page)
	except PageNotAnInteger:
		tests = paginator.page(1)
	except EmptyPage:
		tests = paginator.page(paginator.num_pages)

	for t in tests:
		if ( t.start_time == None or t.start_time < timezone.now()) and ( t.end_time == None or t.end_time > timezone.now()):
			t.status = "Assigned"
		else:
			t.status = "late"

	room = get_object_or_404(Classroom, id=class_id)
	return render(request, 'classroom/view_class.html', {'tests' : tests, 'room' : room } )


@login_required(login_url='login')
@student_required
def done_test(request, class_id):
	taken = list(testTaken.objects.filter(student=request.user).values("test"))

	d = []
	for t in taken: 
		d.append( t['test'] )
	tests = Test.objects.filter(pk__in=d, belongs=class_id)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		tests = Test.objects.filter(belongs=class_id, name__icontains=search).order_by('-create_time')


	# paginator 
	paginator = Paginator(tests, 5)
	page = request.GET.get('page', 1)

	try:
		tests = paginator.page(page)
	except PageNotAnInteger:
		tests = paginator.page(1)
	except EmptyPage:
		tests = paginator.page(paginator.num_pages)


	for t in tests:
		t.status = "done"
		
	room = get_object_or_404(Classroom, id=class_id)
	return render(request, 'classroom/view_class.html', {'tests' : tests, 'room' : room } )