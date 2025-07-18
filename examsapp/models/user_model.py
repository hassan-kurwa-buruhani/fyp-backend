from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Roles(models.TextChoices):
    ADMIN = 'Admin', _('Admin')
    LECTURER = 'Lecturer', _('Lecturer')
    INVIGILATOR = 'Invigilator', _('Invigilator')   
    STUDENT = 'Student', _('Student')

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Roles.choices)
    email = models.EmailField(unique=True)
    device_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
