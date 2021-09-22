from django.urls import path
from .views import add_invitees, \
    validate_email_Send_otp, \
    validate_otp, \
    fetch_details, \
    delete_invitee
# from bbb_api.streaming_helper.helper_streaming import stream_helper

urlpatterns = [
    path('event/meeting/add/invitees/', add_invitees.as_view()),
    path('event/send/otp/', validate_email_Send_otp.as_view()),
    path('event/validate/otp/', validate_otp.as_view()),
    path('event/invitee/details/', fetch_details.as_view()),
    path('event/invitee/delete/', delete_invitee.as_view())



]


