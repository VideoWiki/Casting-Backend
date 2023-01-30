from django.contrib import admin
from .models import KeyDetails, LearningAnalytics, CustomRoomInfo

# Register your models here.

@admin.register(KeyDetails)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')


@admin.register(LearningAnalytics)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'creator_name', 'analytics_url', 'created')


@admin.register(CustomRoomInfo)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('id', 'cast', 'room_type')
