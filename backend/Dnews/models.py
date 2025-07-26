from django.db import models

class NewsArticle(models.Model):
    source = models.CharField(max_length=100)
    title = models.TextField()
    summary = models.TextField()
    link = models.URLField()
    bias = models.CharField(max_length=50, blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    embedded = models.BooleanField(default=False)  # For tracking if sent to vector DB

    def __str__(self):
        return f"{self.source} - {self.title[:50]}"
