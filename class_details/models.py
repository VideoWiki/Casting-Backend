from django.db import models

# Create your models here.

class ClassDetails(models.Model):
    class_id = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10, blank=True, null=True)
    picture = models.CharField(blank=True, null=True, max_length=1000)
    session = models.CharField(blank=True, null=True, max_length=20)
