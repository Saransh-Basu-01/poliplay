from django.db import models
from django.contrib.auth.models import User
import json

class QuizCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Quiz Categories"
    
    def __str__(self):
        return self.name

class QuizQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=500)
    options = models.JSONField(default=list)  # Store as JSON array
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.question_text[:50]}..."

class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(QuizCategory, on_delete=models.SET_NULL, null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    score_percentage = models.FloatField(default=0.0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    time_taken = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Quiz Session {self.session_id}"

class UserAnswer(models.Model):
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.FloatField(default=0.0)  # Time in seconds
    
    class Meta:
        unique_together = ['quiz_session', 'question']
    
    def __str__(self):
        return f"Answer for {self.question.question_text[:30]}..."