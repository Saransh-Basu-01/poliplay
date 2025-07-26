from django.contrib import admin
from .models import QuizCategory, QuizQuestion, QuizSession, UserAnswer

@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'questions_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    
    def questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()
    questions_count.short_description = 'Active Questions'

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'category', 'difficulty', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active', 'created_at']
    search_fields = ['question_text', 'correct_answer']
    readonly_fields = ['created_at']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'category', 'score_percentage', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'category', 'started_at']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['session_id', 'started_at']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_session', 'question_short', 'user_answer_short', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['quiz_session__session_id', 'user_answer']
    
    def question_short(self, obj):
        return obj.question.question_text[:30] + "..."
    question_short.short_description = 'Question'
    
    def user_answer_short(self, obj):
        return obj.user_answer[:30] + "..." if len(obj.user_answer) > 30 else obj.user_answer
    user_answer_short.short_description = 'Answer'