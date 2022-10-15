from django.urls import path
from .views import create_cast
from .join.join import MagicUrlCreator
from .recording.recording import CastRecordingSC
from .room_list.room_list import get_rooms


urlpatterns = [
    path('create/cast/', create_cast.as_view()),
    path('creator/join/cast/', MagicUrlCreator.as_view()),
    path('recording/cast/', CastRecordingSC.as_view()),
    path('cast/list/', get_rooms.as_view()),
]