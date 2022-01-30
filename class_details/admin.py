from django.contrib import admin
from .models import ClassDetails
# Register your models here.


@admin.register(ClassDetails)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_id', 'role', 'email')