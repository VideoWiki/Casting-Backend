from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bbb_api.urls')),
    path('api/', include('cast_invitee_details.urls')),
    path('api/', include('custom_background.urls')),

]
