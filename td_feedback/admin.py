from .models import Feedback, UserCount
from django.contrib import admin


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Feedback)
class UserCountAdmin(admin.ModelAdmin):
    list_display = ('id', )
