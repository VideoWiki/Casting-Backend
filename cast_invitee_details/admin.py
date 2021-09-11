from django.contrib import admin
from .models import CastInviteeDetails
# Register your models here.

@admin.register(CastInviteeDetails)
class CastAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')