from django.urls import path

from .get_cast_info.getcastinfo import GetCastInformation
from .views import add_invitees, \
    fetch_details, \
    delete_invitee
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
from .public_wallet.add_wallet import PublicWalletAdd
from .public_wallet.verify_wallet import PublicWalletVerify
from .public_wallet.mint_nft_update import PublicMintUpdate
from .public_wallet.send_hashed_data import SendHashedIdPublic
from .add_attendee_excel_sheet.excel_add_attendee import ParseExcel
from .nft_drop_mail.gala_cerificate.VCDropMail import NftCertiDropMail
from .nft_drop_mail.post_nft_claim.postNftClaim import postNftMail
from .integration_invitee_list.views import get_invitee_details
from .merkel_tree.save import PostMerkelTreeDetails
from .merkel_tree.fetch import FetchMerkelTreeDetails

urlpatterns = [
    path('event/meeting/add/invitees/', add_invitees.as_view()),
    path('event/send/otp/', SendOtp.as_view()),
    path('event/validate/otp/', ValidateOtp.as_view()),
    path('event/invitee/details/', fetch_details.as_view()),
    path('event/invitee/delete/', delete_invitee.as_view()),
    path('event/add/wallet/address/', AddUser.as_view()),
    path('event/check/email/', CheckEmail.as_view()),
    path('event/users/details/download/', CsvDownloader.as_view()),
    path('event/invitee/details/update/', UptadeInviteeDetails.as_view()),
    path('event/send/wallet/adress/', FetchWalletAdress.as_view()),
    path('event/send/nft/drop/mail/', NftDropMail.as_view()),
    path('event/send/nft/certi/drop/mail/', NftCertiDropMail.as_view()),
    path('event/public/joinee/add/', PublicAddJoinee.as_view()),
    path('event/verify/public/address/', VerifyWalletAddress.as_view()),
    path('event/update/mint/data/', UpdateMintData.as_view()),
    path('event/send/hashed/id/', SendHashedId.as_view()),
    path('event/add/public/wallet/', PublicWalletAdd.as_view()),
    path('event/verify/public/wallet/', PublicWalletVerify.as_view()),
    path('event/mint/update/public/wallet/', PublicMintUpdate.as_view()),
    path('event/send/hashed/id/public/', SendHashedIdPublic.as_view()),
    path('event/invitee/import/', ParseExcel.as_view()),
    path('event/post/vc/details/', postNftMail.as_view()),
    path('get/invitee/details/', get_invitee_details.as_view()),
    path('save/merkel/tree/details/', PostMerkelTreeDetails.as_view()),
    path('get/merkel/tree/details/', FetchMerkelTreeDetails.as_view()),
    path('get/cast/information/', GetCastInformation.as_view()),
]


