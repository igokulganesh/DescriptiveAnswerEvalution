from django.urls import path

from .views import Students, Teachers, Classroom

urlpatterns = [

	# For Classroom
	path('', Classroom.home, name='home'),
	path('dashboard', Classroom.dashboard, name='dashboard'),
	path('<int:class_id>/view_class', Classroom.view_class, name='view_class'),

	path('signup', Classroom.signup, name='signup'),
	path('login', Classroom.login, name='login'),
	path('logout', Classroom.logout, name='logout'),
	
	# For Students 
	path('join_class', Students.join_class, name='join_class'),
	path('<int:test_id>/attend_test', Students.attend_test, name='attend_test'),
	path('<int:test_id>/submit_test', Students.submit_test, name='submit_test'),
	path('<int:test_id>/review_test', Students.review_test, name='review_test'),

	# For Teachers 
	path('create_class', Teachers.create_class, name='create_class'),
	path('<int:class_id>/create_test', Teachers.create_test, name='create_test'),
	path('<int:test_id>/view_test', Teachers.view_test, name='view_test'),
	path('<int:test_id>/create_qn', Teachers.create_qn, name='create_qn'),

]