from django.db import models
from .user_model import User, Roles
from .college_campus_model import CampusSchool, CampusDepartment
from django.core.validators import FileExtensionValidator

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    department = models.ForeignKey('CampusDepartment', on_delete=models.CASCADE, default=" ")
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Lecturer'})

    def __str__(self):
        return f"{self.code} - {self.name}"

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Lecturer'})

    exam_paper = models.FileField(
        upload_to='exam_papers/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True, blank=True
        )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} ({self.course.code} - {self.course.name})"