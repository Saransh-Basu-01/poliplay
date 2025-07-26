from rest_framework import serializers
from .models import Category, Bin, Card, QuizAttempt, QuizAnswer

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ['id', 'name']

class CardSerializer(serializers.ModelSerializer):
    correct = serializers.CharField(source='correct_bin.name', read_only=True)
    
    class Meta:
        model = Card
        fields = ['id', 'text', 'correct']

class CategorySerializer(serializers.ModelSerializer):
    bins = BinSerializer(many=True, read_only=True)
    cards = CardSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'bins', 'cards']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class QuizAnswerSerializer(serializers.ModelSerializer):
    card_id = serializers.IntegerField()
    selected_bin_name = serializers.CharField()
    
    class Meta:
        model = QuizAnswer
        fields = ['card_id', 'selected_bin_name']

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
            card = Card.objects.get(id=answer_data['card_id'])
            selected_bin = Bin.objects.get(
                category=quiz_attempt.category,
                name=answer_data['selected_bin_name']
            )
            is_correct = card.correct_bin == selected_bin
            if is_correct:
                correct_count += 1
                
            QuizAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                card=card,
                selected_bin=selected_bin,
                is_correct=is_correct
            )
        
        quiz_attempt.score = correct_count
        quiz_attempt.total_questions = len(answers_data)
        quiz_attempt.save()
        
        return quiz_attempt