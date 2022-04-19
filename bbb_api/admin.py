from django.contrib import admin
from .models import Meeting, TemporaryFiles, NftDetails, ViewerDetails
# Register your models here.


@admin.register(Meeting)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name')


@admin.register(TemporaryFiles)
class TempAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(NftDetails)
class TempAdmin(admin.ModelAdmin):
    list_display = ('id','cast', 'mint_function_name', 'contract_address', 'parameter', 'image', 'description')


@admin.register(ViewerDetails)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('id', 'cast', 'force_listen_only', 'enable_screen_sharing', 'enable_webcam')