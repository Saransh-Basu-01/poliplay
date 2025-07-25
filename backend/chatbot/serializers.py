from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answer_text', 'language', 'created_at']

class QuestionRequestSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    language = serializers.CharField(max_length=10, default='en')