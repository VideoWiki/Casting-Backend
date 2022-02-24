from django.urls import path
from .views import add_invitees, \
    fetch_details, \
    delete_invitee
from cast_invitee_details.joinee_details.joineedetails import JoineeDetails, FetchJoineeDetails
from .add_wallet_address.addMetamaskAddress import AddUser
from .email_checker.email_checker import CheckEmail
from .otp.send_otp import SendOtp
from .otp.validate_otp import ValidateOtp
from .csv_downloader.csv_downloader import CsvDownloader
from .update_invitee_details.update_invitee_details import UptadeInviteeDetails
from .send_wallet_address.FetchWalletAdress import FetchWalletAdress
from .nft_drop_mail.nftDropMail import NftDropMail
from .public_add_joinee.PublicAddJoinee import PublicAddJoinee
from .verify_wallet_address.VerifyWalletAddress import VerifyWalletAddress
from .update_mint_data.UpdateMintData import UpdateMintData
from .verify_wallet_address.send_hashd_id import SendHashedId


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
    path('event/users/details/download/', CsvDownloader.as_view()),
    path('event/invitee/details/update/', UptadeInviteeDetails.as_view()),
    path('event/send/wallet/adress/', FetchWalletAdress.as_view()),
    path('event/send/nft/drop/mail/', NftDropMail.as_view()),
    path('event/public/joinee/add/', PublicAddJoinee.as_view()),
    path('event/verify/public/address/', VerifyWalletAddress.as_view()),
    path('event/update/mint/data/', UpdateMintData.as_view()),
    path('event/send/hashed/id/', SendHashedId.as_view()),
]


