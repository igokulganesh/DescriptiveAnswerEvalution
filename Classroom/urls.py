from django.urls import path

from .views import Students, Teachers, Classroom

urlpatterns = [

	# For Classroom
	path('', Classroom.home, name='home'),
	path('dashboard', Classroom.dashboard, name='dashboard'),
	path('view_class', Classroom.view_class, name='view_class'),

	path('signup', Classroom.signup, name='signup'),
	path('login', Classroom.login, name='login'),
	path('logout', Classroom.logout, name='logout'),
	
	# For Students 
	path('join_class', Students.join_class, name='join_class'),

	# For Teachers 
	path('create', Teachers.create_class, name='create_class'),

]