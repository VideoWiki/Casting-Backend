from django.urls import path
from .views import create_event, join_meeting, delete_meeting,\
    is_meeting_running, meeting_info, meetings, get_recordings, \
    user_recordings, scheduled_meetings, meeting_type_checker, \
    my_events



urlpatterns = [
    path('event/meeting/create/', create_event.as_view()),
    path('event/meeting/join/', join_meeting.as_view()),
    path('event/meetings/', meetings.as_view()),
    path('event/meeting/delete/', delete_meeting.as_view()),
    path('event/meeting/running/', is_meeting_running.as_view()),
    path('event/meeting/info/', meeting_info.as_view()),
    path('event/recordings/', get_recordings.as_view()),
    path('event/user/recordings/', user_recordings.as_view()),
    path('event/scheduled/meetings/', scheduled_meetings.as_view()),
    path('event/meeting/type/', meeting_type_checker.as_view()),
    path('event/user/events/', my_events.as_view()),
]


