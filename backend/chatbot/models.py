from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    answer_text = models.TextField()
    language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.question_text[:50]}..."

    class Meta:
        ordering = ['-created_at']

class Document(models.Model):
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded_at']