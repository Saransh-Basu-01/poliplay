from rest_framework import serializers
from .models import QuizQuestion, QuizSession, UserAnswer, QuizCategory

class QuizCategorySerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizCategory
        fields = ['id', 'name', 'description', 'is_active', 'questions_count']
    
    def get_questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()

class QuizQuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'options', 'difficulty', 'category_name', 'created_at']
        # Don't expose correct_answer in list/retrieve

class QuizQuestionWithAnswerSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'correct_answer', 'options', 'difficulty', 'explanation', 'category_name']

class QuizSessionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizSession
        fields = ['id', 'session_id', 'category_name', 'total_questions', 'correct_answers', 
                 'score_percentage', 'started_at', 'completed_at', 'is_completed', 'duration']
    
    def get_duration(self, obj):
        if obj.time_taken:
            return obj.time_taken.total_seconds()
        return None

class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuizQuestionWithAnswerSerializer(read_only=True)
    
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'user_answer', 'is_correct', 'answered_at', 'time_taken']

class SubmitAnswerSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100)
    question_id = serializers.IntegerField()
    answer = serializers.CharField(max_length=500)
    time_taken = serializers.FloatField(default=0.0)

class GenerateQuestionSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200, required=False)
    category = serializers.CharField(max_length=100, required=False, default="General")
    difficulty = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard'], 
        required=False,
        default='medium'
    )
    count = serializers.IntegerField(min_value=1, max_value=20, default=5)

class StartQuizSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)
    difficulty = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard'], 
        required=False,
        default='medium'
    )
    question_count = serializers.IntegerField(min_value=1, max_value=50, default=10)
    generate_new = serializers.BooleanField(default=False)
    topics = serializers.ListField(
        child=serializers.CharField(max_length=200),
        required=False,
        allow_empty=True
    )