from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Classroom, Enrollment, Test, Question, Answer, testTaken
from ..decorators import teacher_required
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse

def home(request):
	return render(request, 'classroom/home.html' )

@login_required(login_url='login')
def dashboard(request):
	colors = ['blue', 'orange', 'green', 'red', 'purple', 'pink' ]
	
	if request.user.is_staff:
		rooms = Classroom.objects.filter(owner=request.user).values()
	else:
		enroll = list(Enrollment.objects.filter(student=request.user).values('room_id'))
		d = []
		for e in enroll: 
			d.append( e['room_id'] )
		rooms = Classroom.objects.filter(pk__in=d).values()

	rooms = list(rooms)
	for i in range(len(rooms)):
		rooms[i]["color"] = colors[i%6]
		rooms[i]["delay"] = i+2 * 100  

	return render(request, 'classroom/dashboard.html', { 'rooms' : rooms })

@login_required(login_url='login')
def view_class(request, class_id):
	tests = Test.objects.filter(belongs=class_id).order_by('-create_time')

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


	if request.user.is_staff == False :
		for t in tests:
			if testTaken.objects.filter(student=request.user, test=t).exists():
				t.status = "done"
			elif ( t.start_time == None or t.start_time < timezone.now()) and ( t.end_time == None or t.end_time > timezone.now()):
				t.status = "Assigned"
			else:
				t.status = "late"

	room = get_object_or_404(Classroom, id=class_id)

	return render(request, "classroom/view_class.html", {'tests' : tests, 'room' : room } )


@login_required(login_url='login')
def people(request, class_id):
	teacher = get_object_or_404(Classroom, id=class_id).owner
	enroll = Enrollment.objects.filter(room=class_id)

	student = [] 
	for e in enroll:
		student.append(e.student)
	
	print(student)
	return render(request, "classroom/people.html", { 'teacher' : teacher, 'student' : student })


def signup(request):
	if request.method == "POST":
		name 	 = request.POST['name']
		email 	 = request.POST['email'] # Email as username
		password = request.POST['password']

		is_staff = request.POST.get('is_staff', False)

		if is_staff == 'on':
			is_staff = True 
		else: 
			is_staff = False

		user = User.objects.create_user(first_name=name, email=email, username=email, password=password, is_staff=is_staff)
		user.save()

		# user = authenticate(username=email, password=password)
		# auth_login(request, user)

		return redirect('login')

	return render(request, 'classroom/login.html')

def login(request):
	if request.method == "POST": 
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username=email, password=password)

		if user is not None:
			auth_login(request, user)
			return redirect('dashboard')
		else:
			messages.error(request,'Username or password incorrect')
	return render(request, 'classroom/login.html')

def logout(request):
	auth_logout(request)
	return redirect('home')