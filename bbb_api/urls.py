from django.urls import path
from .create_event_api.views import create_event
from .join_event_api.views import join_meeting
from .delete_event_api.views import delete_meeting
from .all_running_events.running_events import meetings
from .is_event_running.event_status import event_status
from .get_event_info.event_info import meeting_info
from .my_recordings_api.views import user_recordings
from .all_scheduled_events.scheduled_events import scheduled_meetings
from .event_type_checker.event_type_checker import meeting_type_checker
from .my_events_api.views import get_my_events
from bbb_api.create_event_api.upload_media import FileUploadView
from .event_recording.event_recording import event_recording
from bbb_api.update_cast.update_cast import update_cast
from bbb_api.update_cast.get_details import get_details
# from bbb_api.streaming_helper.helper_streaming import stream_helper
from bbb_api.my_recordings_api.event_recording import CastRecording


urlpatterns = [
    path('event/meeting/create/', create_event.as_view()),
    path('event/meeting/join/', join_meeting.as_view()),
    path('event/meetings/', meetings.as_view()),
    path('event/meeting/delete/', delete_meeting.as_view()),
    path('event/meeting/running/', event_status.as_view()),
    path('event/meeting/info/', meeting_info.as_view()),
    path('event/user/recordings/', user_recordings.as_view()),
    path('event/scheduled/events/', scheduled_meetings.as_view()),
    path('event/meeting/type/', meeting_type_checker.as_view()),
    path('event/user/events/', get_my_events.as_view()),
    path('event/user/upload/media/', FileUploadView.as_view()),
    path('event/meeting/update/', update_cast.as_view()),
    path('event/meeting/get/details/', get_details.as_view()),
    path('event/meeting/recording/', CastRecording.as_view())
]


