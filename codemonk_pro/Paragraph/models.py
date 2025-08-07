from django.db import models
from apps.users.models import CustomUser

class Paragraph(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class WordFrequency(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    word = models.CharField(max_length=64)
    frequency = models.IntegerField(default=0)
    class Meta:
        unique_together = ('user', 'word')

