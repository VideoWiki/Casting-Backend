from django.contrib import admin
from .models import Meeting, TemporaryFiles, NftDetails
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