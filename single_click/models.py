from django.db import models
from rest_framework_api_key.models import APIKey


class KeyDetails(models.Model):
    key = models.ForeignKey(APIKey, on_delete=models.CASCADE, null=True, blank=True)
    room_limit = models.IntegerField(default=100, blank=True, null=True)
    room_count = models.IntegerField(default=0,blank=True, null=True)


class LearningAnalytics(models.Model):
    room_name = models.CharField(blank=True, null=True, max_length=200)
    creator_name = models.CharField(blank=True, null=True, max_length=200)
    analytics_url = models.CharField(blank=True, null=True, max_length=500)
    created = models.DateTimeField(auto_now_add=True)
