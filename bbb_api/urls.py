from django.urls import path
from .views import create_event, join_meeting, delete_meeting, is_meeting_running, meeting_info, meetings

urlpatterns = [
    path('meeting/create/', create_event.as_view()),
    path('meeting/join/', join_meeting.as_view()),
    path('meetings/', meetings.as_view()),
    path('meeting/delete/', delete_meeting.as_view()),
    path('meeting/running/', is_meeting_running.as_view()),
    path('meeting/info/', meeting_info.as_view()),
]


