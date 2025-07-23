from django.db import models
from .course_exam_model import Exam

class QuestionType(models.TextChoices):
    MCQ = 'MCQ', 'Multiple Choice'
    TRUE_FALSE = 'TRUE_FALSE', 'True or False'
    MATCHING = 'MATCHING', 'Matching Items'
    SHORT = 'SHORT', 'Short Answer'
    OPEN = 'OPEN', 'Open Ended'

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
      # e.g. Question 1, 2, 3...

    def __str__(self):
        return f"Q{self.number}: {self.text[:50]}"