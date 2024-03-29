from django.db import models
from bbb_api.models import Meeting
# Create your models here.


class CastInviteeDetails(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    # nft_types = (('simple', 'Simple'),
    #              ('vc', 'VC'))
    # nft_type = models.CharField(max_length=100, choices=nft_types, blank=True, null=True)
    # name = models.CharField(max_length=20, blank=True, null= True)
    email = models.EmailField(max_length=50, blank= True, null= True)
    role = models.CharField(max_length= 20, blank=True, null=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of opt_sent')
    verified = models.CharField(max_length=10, blank=True, null=True, default=False)
    metamask_address = models.CharField(max_length=100, blank=True, null=True)
    metamask_verified = models.CharField(max_length=10, blank=True, null=True)
    nft_enable = models.BooleanField(default=False, blank=True, null=True)
    vc_enable = models.BooleanField(default=False, blank=True, null=True)
    joined = models.BooleanField(default=False, blank=True, null=True)
    invited = models.BooleanField(default=False, blank=True, null=True)
    mint_status = (
        ('not started', 'Not Started'),
        ('started', 'Started'),
        ('successful', 'Successful')
    )
    mint = models.CharField(max_length=100, choices=mint_status, blank=True, null=True)
    vc_mint = models.CharField(max_length=100, choices=mint_status, blank=True, null=True)
    mint_count = models.IntegerField(default=0)
    vc_mint_count = models.IntegerField(default=0)
    transaction_id = models.CharField(max_length= 300, blank=True, null=True)
    vc_transaction_id = models.CharField(max_length=300, blank=True, null=True)
    nft_mail_sent = models.BooleanField(blank=True, null=True, default=False)
    vc_nft_mail_sent = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        unique_together = ('cast', 'metamask_address')


class PublicWallet(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    mint_status = (
        ('not started', 'Not Started'),
        ('started', 'Started'),
        ('successful', 'Successful')
    )
    metamask_address = models.CharField(max_length=100, blank=True, null=True)
    metamask_verified = models.CharField(max_length=10, blank=True, null=True)
    mint = models.CharField(max_length=100, choices=mint_status, blank=True, null=True)
    mint_count = models.IntegerField(default=0)
    transaction_id = models.CharField(max_length=300, blank=True, null=True)
    class Meta:
        unique_together = ('cast', 'metamask_address')

class MerkelTreeDetail(models.Model):
    cast = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    data = models.CharField(max_length=10000, blank=True, null=True)
