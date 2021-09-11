from django.urls import path
from .views import add_invitees
# from bbb_api.streaming_helper.helper_streaming import stream_helper

urlpatterns = [
path('event/meeting/add/invitees/', add_invitees.as_view()),

]


