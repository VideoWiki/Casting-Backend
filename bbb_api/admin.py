from django.contrib import admin
from .models import Meeting, TemporaryFiles
# Register your models here.
@admin.register(Meeting)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name')

@admin.register(TemporaryFiles)
class TempAdmin(admin.ModelAdmin):
    list_display = ('id',)