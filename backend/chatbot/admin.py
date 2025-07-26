from django.contrib import admin
from .models import Question, Document

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'language', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('question_text', 'answer_text')
    readonly_fields = ('created_at',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_processed', 'uploaded_at')
    list_filter = ('is_processed', 'uploaded_at')
    search_fields = ('name', 'file_path')