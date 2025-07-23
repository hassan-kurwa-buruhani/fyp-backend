from django.db import models
from .user_model import User
from .course_exam_model import Exam
from .question_model import Question

class LecturerAnswer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    subanswers = models.JSONField()  # Example: {"i": "A", "ii": "B"} or {"main": "The answer"}

class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    subanswers = models.JSONField()
    score = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'exam', 'question')