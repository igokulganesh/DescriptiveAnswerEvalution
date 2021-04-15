from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Classroom(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE) # Teacher 
	name = models.CharField(max_length=255) # class name 
	code = models.CharField(max_length=5, unique=True) # code for students to join 
	desc = models.CharField(max_length=255, blank=True) # class Description for optional

	def __str__(self):
		return self.name

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     classes = models.ManyToManyField(Classroom, related_name='students', blank=True, through='Enrollment')

#     def __str__(self):
#         return self.user.first_name

class Enrollment(models.Model):
	class Meta:
		unique_together = (('room', 'student'),)
	
	room =  models.ForeignKey(Classroom, on_delete=models.CASCADE)
	student = models.ForeignKey(User, on_delete=models.CASCADE) # students enrolled 

class Test(models.Model):
	belongs = models.ForeignKey(Classroom, on_delete=models.CASCADE) 
	name = models.CharField(max_length=255)
	desc = models.CharField(max_length=2555, blank=True)
	create_time = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
	# test_mark = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.name

class testTaken(models.Model):
	class Meta:
		unique_together = (('test', 'student'),)
	
	test =  models.ForeignKey(Test, on_delete=models.CASCADE)
	student = models.ForeignKey(User, on_delete=models.CASCADE) 
	submittedAt = models.DateTimeField(blank=True, null=True)

class Question(models.Model):
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
	qn_text = models.CharField('Question', max_length=2000)
	key = models.CharField('Answer key', max_length=5000)
	max_score = models.PositiveSmallIntegerField(default=100)

	def __str__(self):
		return self.qn_text

class Answer(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer_text = models.CharField(max_length=10000)
	ml_score = models.PositiveSmallIntegerField(default=0)
	actual_score = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.answer_text
