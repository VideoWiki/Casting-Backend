from django.urls import path
from .create_event_api.views import create_event
# from .join_event_api.views import join_meeting
from .delete_event_api.views import delete_meeting
from .all_running_events.running_events import meetings
from .is_event_running.event_status import event_status
from .get_event_info.event_info import meeting_info
from .my_recordings_api.views import user_recordings
from .all_scheduled_events.scheduled_events import scheduled_meetings
from .event_type_checker.event_type_checker import meeting_type_checker
from .my_events_api.views import get_my_events
from bbb_api.create_event_api.upload_media import FileUploadView
from bbb_api.update_cast.update_cast import update_cast
from bbb_api.update_cast.get_details import get_details
from bbb_api.my_recordings_api.event_recording import CastRecording
from bbb_api.fetch_nft_details.NftDetails import FetchNftDetails
from bbb_api.activate_public_nft.activate_public_nft import NftActivatePublic
from bbb_api.stream.start import start_stream
from bbb_api.stream.end import end_stream
from bbb_api.join_event_api.join import join_meeting
from bbb_api.nft.nft_details import AudienceAirdrop
from bbb_api.join_event_api.magic_url import MagicUrl
from bbb_api.get_template.get import GetTemplate
from bbb_api.get_template.update import UpdateTemplate
from bbb_api.send_test_mail.views import SendTestMail
from bbb_api.get_template.reset import ResetTemplate


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
    path('event/meeting/recording/', CastRecording.as_view()),
    path('event/fetch/nft/details/', FetchNftDetails.as_view()),
    path('event/nft/activate/public/', NftActivatePublic.as_view()),
    path('event/ls/start/', start_stream.as_view()),
    path('event/ls/end/', end_stream.as_view()),
    path('event/add/nft/details/', AudienceAirdrop.as_view()),
    path('event/join/', MagicUrl.as_view()),
    path('event/get/template/', GetTemplate.as_view()),
    path('event/update/template/', UpdateTemplate.as_view()),
    path('event/send/test/mail/', SendTestMail.as_view()),
    path('event/reset/template/', ResetTemplate.as_view())


]


