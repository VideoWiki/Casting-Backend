from django.urls import path
from .views import add_invitees, \
    fetch_details, \
    delete_invitee
from cast_invitee_details.joinee_details.joineedetails import JoineeDetails, FetchJoineeDetails
from .add_wallet_address.addMetamaskAddress import AddUser
from .email_checker.email_checker import CheckEmail
from .otp.send_otp import SendOtp
from .otp.validate_otp import ValidateOtp

urlpatterns = [
    path('event/meeting/add/invitees/', add_invitees.as_view()),
    path('event/send/otp/', SendOtp.as_view()),
    path('event/validate/otp/', ValidateOtp.as_view()),
    path('event/invitee/details/', fetch_details.as_view()),
    path('event/invitee/delete/', delete_invitee.as_view()),
    path('event/joinee/add/', JoineeDetails.as_view()),
    path('event/joinee/details/', FetchJoineeDetails.as_view()),
    path('event/add/wallet/address/', AddUser.as_view()),
    path('event/check/email/', CheckEmail.as_view()),



]


