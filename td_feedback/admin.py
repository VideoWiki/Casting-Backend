from .models import Feedback, UserCount
from django.contrib import admin


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(UserCount)
class UserCountAdmin(admin.ModelAdmin):
    list_display = ('id', )
