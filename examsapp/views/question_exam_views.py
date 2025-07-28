from rest_framework import generics
from examsapp.models import Question, Answer
from examsapp.serializers import QuestionSerializer, AnswerSerializer

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
