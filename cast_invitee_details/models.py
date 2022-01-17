from django.db import models
from bbb_api.models import Meeting
# Create your models here.


class CastInviteeDetails(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True, null= True)
    email = models.EmailField(max_length=50, blank= True, null= True)
    role = models.CharField(max_length= 10, blank=True, null=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of opt_sent')
    verified = models.CharField(max_length=10, blank=True, null=True)
    metamask_address = models.CharField(max_length=100, blank=True, null=True)
    metamask_verified = models.CharField(max_length=10, blank=True, null=True)



class CastJoineeDetails(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    # avatar = models.ImageField(blank=True, null=True, upload_to= 'avatar_images')


