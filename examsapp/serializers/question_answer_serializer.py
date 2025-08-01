from rest_framework import serializers
from examsapp.models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id','question_number', 'question_text', 'marks', 'exam']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'ai_answer']
