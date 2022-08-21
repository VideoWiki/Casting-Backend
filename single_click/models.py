from django.db import models
from rest_framework_api_key.models import APIKey


class KeyDetails(models.Model):
    key = models.ForeignKey(APIKey, on_delete=models.CASCADE, null=True, blank=True)
    room_limit = models.IntegerField(default=100, blank=True, null=True)
    room_count = models.IntegerField(default=0,blank=True, null=True)