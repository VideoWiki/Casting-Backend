from django.db import models
from bbb_api.models import Meeting
# Create your models here.

class CastInviteeDetails(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True, null= True)
    email = models.EmailField(max_length=50, blank= True, null= True)
    role = models.CharField(max_length= 10, blank=True, null=True)


