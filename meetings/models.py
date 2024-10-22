from django.db import models

class Transcript(models.Model):
    source = models.CharField(max_length=50)  # e.g., Fireflies
    tags = models.ManyToManyField('Tag', related_name='transcripts', blank=True)
    meeting_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source} - {self.title}"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name