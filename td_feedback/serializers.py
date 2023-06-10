# feedback/serializers.py

from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['sender', 'receiver', 'room_id', 'feedback_text', 'created_at']
