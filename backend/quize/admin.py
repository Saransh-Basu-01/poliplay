from django.contrib import admin
from .models import Category, Bin, Card, QuizAttempt, QuizAnswer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'category__name']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['text', 'category', 'correct_bin', 'created_at']
    list_filter = ['category', 'correct_bin']
    search_fields = ['text']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'category', 'score', 'total_questions', 'started_at']
    list_filter = ['category', 'started_at']
    readonly_fields = ['started_at', 'completed_at']

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempt', 'card', 'selected_bin', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']