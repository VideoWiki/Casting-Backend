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
    verified = models.CharField(max_length=10, blank=True, null=True, default=False)
    metamask_address = models.CharField(max_length=100, blank=True, null=True)
    metamask_verified = models.CharField(max_length=10, blank=True, null=True)
    nft_enable = models.BooleanField(default=False, blank=True, null=True)
    joined = models.BooleanField(default=False, blank=True, null=True)
    invited = models.BooleanField(default=False, blank=True, null=True)
    mint_status = (
        ('not started', 'Not Started'),
        ('started', 'Started'),
        ('successful', 'Successful')
    )
    mint = models.CharField(max_length=100, choices=mint_status, blank=True, null=True)
    mint_count = models.IntegerField(default=0)
    transaction_id = models.CharField(max_length= 300, blank=True, null=True)
    nft_mail_sent = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        unique_together = ('cast', 'metamask_address')


class CastJoineeDetails(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    # avatar = models.ImageField(blank=True, null=True, upload_to= 'avatar_images')


