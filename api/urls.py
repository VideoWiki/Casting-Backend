from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bbb_api.urls')),
    path('api/', include('cast_invitee_details.urls')),
    path('api/', include('custom_background.urls')),
    path('api/', include('class_details.urls')),
    path('api/', include('single_click.urls')),
    path('api/', include('add_text_to_image.urls')),
    path('api/', include('td_feedback.urls')),

]
