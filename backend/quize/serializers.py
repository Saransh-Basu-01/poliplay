from rest_framework import serializers
from .models import Category, Question, Option, QuizAttempt, QuizAnswer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'correct_answer', 'options']

class CategorySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'questions']

class CategoryListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'question_count']
    
    def get_question_count(self, obj):
        return obj.questions.count()

class QuizAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    selected_answer = serializers.CharField()
    
    class Meta:
        model = QuizAnswer
        fields = ['question_id', 'selected_answer']

class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, write_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user_name', 'category', 'category_name', 'score', 'total_questions', 'started_at', 'completed_at', 'answers']
        read_only_fields = ['score', 'started_at', 'completed_at']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        quiz_attempt = QuizAttempt.objects.create(**validated_data)
        
        correct_count = 0
        for answer_data in answers_data:
            question = Question.objects.get(id=answer_data['question_id'])
            selected_answer = answer_data['selected_answer']
            is_correct = question.correct_answer == selected_answer
            if is_correct:
                correct_count += 1
                
            QuizAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
        
        quiz_attempt.score = correct_count
        quiz_attempt.total_questions = len(answers_data)
        quiz_attempt.save()
        
        return quiz_attempt