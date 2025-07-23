from django.contrib import admin
from .models import User, Roles, Course, Exam, Question, QuestionType, LecturerAnswerSheet, StudentAnswerSheet, LecturerAnswer, StudentAnswer

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(LecturerAnswerSheet)
admin.site.register(StudentAnswerSheet)
admin.site.register(LecturerAnswer)
admin.site.register(StudentAnswer)
