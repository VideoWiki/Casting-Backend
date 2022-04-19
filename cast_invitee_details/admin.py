from django.contrib import admin
from .models import CastInviteeDetails, PublicWallet
# Register your models here.

@admin.register(CastInviteeDetails)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'nft_enable')


@admin.register(PublicWallet)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'metamask_address', 'mint', 'mint_count', 'metamask_verified', 'transaction_id')


