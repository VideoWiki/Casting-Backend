from django.db import models

class NftCertificateImage(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='gala_NFT', blank=True, null=True)
