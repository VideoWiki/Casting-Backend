from django.contrib import admin
from .models import NftCertificateImage

@admin.register(NftCertificateImage)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
