from celery import shared_task
from .models import Paragraph, WordFrequency
from django.db import transaction
from apps.users.models import CustomUser

@shared_task
def process_paragraphs(paragraph_ids, user_id):
    user = CustomUser.objects.get(id=user_id)
    word_counts = {}
    for pid in paragraph_ids:
        para = Paragraph.objects.get(id=pid)
        words = para.text.lower().split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    with transaction.atomic():
        for word, count in word_counts.items():
            obj, _ = WordFrequency.objects.get_or_create(user=user, word=word)
            obj.frequency += count
            obj.save()
