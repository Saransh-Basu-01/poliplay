from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Bin(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='bins')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Card(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cards')
    text = models.TextField()
    correct_bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='correct_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:50]}..."

class QuizAttempt(models.Model):
    user_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Quiz {self.id} - {self.category.name} - {self.score}/{self.total_questions}"

class QuizAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    selected_bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer {self.id} - {'Correct' if self.is_correct else 'Wrong'}"