from django.contrib import admin
from .models import CastInviteeDetails, CastJoineeDetails
# Register your models here.

@admin.register(CastInviteeDetails)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'nft_enable')


@admin.register(CastJoineeDetails)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)