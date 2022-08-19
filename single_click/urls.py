from django.urls import path
from .views import create_cast
from .join.join import MagicUrlCreator
from .recording.recording import CastRecordingSC


urlpatterns = [
    path('create/cast/', create_cast.as_view()),
    path('creator/join/cast/', MagicUrlCreator.as_view()),
    path('recording/cast/', CastRecordingSC.as_view()),
    ]