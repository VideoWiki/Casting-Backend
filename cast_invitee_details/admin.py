from django.contrib import admin
from .models import CastInviteeDetails, PublicWallet, MerkelTreeDetail
# Register your models here.

@admin.register(CastInviteeDetails)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'role', 'nft_enable')


@admin.register(PublicWallet)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'metamask_address', 'mint', 'mint_count', 'metamask_verified', 'transaction_id')

@admin.register(MerkelTreeDetail)
class MerkelTreeDetail(admin.ModelAdmin):
    list_display = ('id', 'cast_id', 'data',)
