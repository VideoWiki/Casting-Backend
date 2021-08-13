from django.contrib import admin
from .models import background_pictures
# Register your models here.

# admin.site.register(background_pictures)
@admin.register(background_pictures)
class bg_images(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'picture_url')
    ordering = ('id',)

