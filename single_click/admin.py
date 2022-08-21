from django.contrib import admin
from .models import KeyDetails
# Register your models here.

@admin.register(KeyDetails)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')