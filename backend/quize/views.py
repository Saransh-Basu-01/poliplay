from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import Category, Card, QuizAttempt
from .serializers import (
    CategorySerializer, 
    CategoryListSerializer, 
    QuizAttemptSerializer
)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related('bins', 'cards__correct_bin')
    serializer_class = CategorySerializer
    lookup_field = 'name'

class QuizSubmitView(generics.CreateAPIView):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz_attempt = serializer.save()
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        
        return Response({
            'quiz_id': quiz_attempt.id,
            'score': quiz_attempt.score,
            'total_questions': quiz_attempt.total_questions,
            'percentage': round((quiz_attempt.score / quiz_attempt.total_questions) * 100, 2)
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def quiz_stats(request):
    total_attempts = QuizAttempt.objects.count()
    if total_attempts == 0:
        return Response({
            'total_attempts': 0,
            'average_score': 0,
            'categories': []
        })
    
    category_stats = []
    for category in Category.objects.all():
        attempts = QuizAttempt.objects.filter(category=category)
        if attempts.exists():
            avg_score = sum(attempt.score for attempt in attempts) / attempts.count()
            category_stats.append({
                'category': category.name,
                'attempts': attempts.count(),
                'average_score': round(avg_score, 2)
            })
    
    overall_avg = sum(attempt.score for attempt in QuizAttempt.objects.all()) / total_attempts
    
    return Response({
        'total_attempts': total_attempts,
        'average_score': round(overall_avg, 2),
        'categories': category_stats
    })