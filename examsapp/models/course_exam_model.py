from django.db import models
from .user_model import User

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Lecturer'})

    def __str__(self):
        return f"{self.code} - {self.name}"

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.course.code} - {self.course.name})"