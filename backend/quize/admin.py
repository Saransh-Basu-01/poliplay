from django.contrib import admin
from .models import Category, Question, Option, QuizAttempt, QuizAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Show 4 option fields by default
    max_num = 5  # Maximum 5 options per question

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_question_count', 'created_at']
    search_fields = ['name']
    
    def get_question_count(self, obj):
        return obj.questions.count()
    get_question_count.short_description = 'Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'category', 'correct_answer', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['question_text', 'correct_answer']
    inlines = [OptionInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['option_text', 'question', 'created_at']
    list_filter = ['question__category']
    search_fields = ['option_text']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'category', 'score', 'total_questions', 'get_percentage', 'started_at']
    list_filter = ['category', 'started_at']
    readonly_fields = ['started_at', 'completed_at']
    
    def get_percentage(self, obj):
        if obj.total_questions > 0:
            return f"{round((obj.score / obj.total_questions) * 100, 1)}%"
        return "0%"
    get_percentage.short_description = 'Percentage'

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempt', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at', 'question__category']