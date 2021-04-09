from django.contrib import admin
from .models import Classroom, Enrollment, Test, Question, Answer

admin.site.register(Classroom)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Enrollment)

