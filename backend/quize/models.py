from django.db import models
from django.core.validators import MinLengthValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def question_count(self):
        return self.questions.filter(is_active=True).count()

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(validators=[MinLengthValidator(10)])
    correct_answer = models.CharField(max_length=200)
    explanation = models.TextField(blank=True, null=True)
    difficulty_level = models.CharField(
        max_length=10, 
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.question_text[:50]}..."

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.option_text

class QuizAttempt(models.Model):
    user_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    time_taken = models.DurationField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Quiz {self.id} - {self.category.name} - {self.score}/{self.total_questions}"

    @property
    def percentage(self):
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100, 2)
        return 0

# Updated QuizAnswer model with proper defaults and null handling
class QuizAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    # Make question nullable temporarily for migration
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    # Make selected_answer have a default
    selected_answer = models.CharField(max_length=200, default='')
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['answered_at']

    def __str__(self):
        return f"Answer {self.id} - {'Correct' if self.is_correct else 'Wrong'}"