# feedback/models.py

from django.db import models

class Feedback(models.Model):
    sender = models.CharField(blank=True, null=True, max_length=200)
    receiver = models.CharField(blank=True, null=True, max_length=200)
    room_id = models.CharField(max_length=100, blank=True)
    feedback_text = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserCount(models.Model):
    room_id = models.CharField(max_length=50)
    user_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_id

