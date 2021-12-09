from django.urls import path
from .views import TimezoneView, AllTimezones
urlpatterns = [
    path('top/tz/', TimezoneView.as_view()),
    path('all/tz/', AllTimezones.as_view())
    ]