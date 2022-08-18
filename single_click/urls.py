from django.urls import path
from .views import create_cast
from .join.join import MagicUrlSC

urlpatterns = [
    path('create/cast/', create_cast.as_view()),
    path('join/cast/', MagicUrlSC.as_view()),
    ]