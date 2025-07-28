
from django.db import models
from examsapp.models import Question  

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    ai_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question}"
