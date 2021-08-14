from django.urls import path
from .create_event_api.views import create_event
from .join_event_api.views import join_meeting
from .delete_event_api.views import delete_meeting
from .all_running_events.all_running_events import meetings
from .is_event_running.is_event_running import is_meeting_running
from .get_event_info.event_info_api import meeting_info
from .my_recordings_api.views import user_recordings
from .all_scheduled_events.all_scheduled_events import scheduled_meetings
from .event_type_checker.event_type_checker import meeting_type_checker
from .my_events_api.views import get_my_events


urlpatterns = [
    path('event/meeting/create/', create_event.as_view()),
    path('event/meeting/join/', join_meeting.as_view()),
    path('event/meetings/', meetings.as_view()),
    path('event/meeting/delete/', delete_meeting.as_view()),
    path('event/meeting/running/', is_meeting_running.as_view()),
    path('event/meeting/info/', meeting_info.as_view()),
    # path('event/recordings/', get_recordings.as_view()),
    path('event/user/recordings/', user_recordings.as_view()),
    path('event/scheduled/events/', scheduled_meetings.as_view()),
    path('event/meeting/type/', meeting_type_checker.as_view()),
    path('event/user/events/', get_my_events.as_view()),
]


