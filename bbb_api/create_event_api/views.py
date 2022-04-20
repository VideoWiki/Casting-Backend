import pytz
from rest_framework.views import APIView
from ..models import Meeting, NftDetails, ViewerDetails
from rest_framework.response import Response
from library.helper import private_meeting_id_generator, \
    public_meeting_id_generator, user_info, \
    user_info_email, generate_random_key, \
    user_info_name
from rest_framework import status
from api.global_variable import BASE_URL, BASE_DIR, VW_RTMP_URL
from ..create_event_email_sender import time_convertor, tc
from .helper import invite_mail
import datetime
from .start_now_func import start_cast_now
import json
import ast

class create_event(APIView):
    def post(self, request):
        meeting = Meeting()
        name = request.data['event_name']
        if name == "":
            return Response({
                "status": False,
                "message": "cast name can't be empty"
            }, status=status.HTTP_400_BAD_REQUEST)
        meeting.event_name = name
        # if Meeting.objects.filter(event_name__iexact=name):
        #     return Response({
        #         "status": False,
        #         "message": "event with this name is already present"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # else:
        #     meeting.event_name = name
        meeting.private_meeting_id = private_meeting_id_generator()
        meeting.public_meeting_id = public_meeting_id_generator()
        meeting.meeting_type = request.data['meeting_type']
        if meeting.meeting_type == "":
            meeting.meeting_type = "private"
        attendee_password = request.data['attendee_password']

        if attendee_password == '':
            random_password = generate_random_key()
            meeting.attendee_password = random_password
        else:
            meeting.attendee_password = attendee_password

        mod_password = request.data['moderator_password']

        if mod_password == '':
            random_password = generate_random_key()
            meeting.moderator_password = random_password
        else:
            meeting.moderator_password = mod_password

        viewer_password = request.data["viewer_password"]
        if viewer_password == '':
            random_password = generate_random_key()
            meeting.viewer_password = random_password
        else:
            meeting.viewer_password = viewer_password

        mode_viewer = request.data["viewer_mode"]
        if mode_viewer == "True":
            mode_viewer = True
            meeting.viewer_mode = True
        else:
            meeting.viewer_mode = False
        meeting.max_participant = request.data['max_participant']
        meeting.moderator_only_text = request.data['moderator_only_text']
        meeting.welcome = request.data['welcome_text']
        meeting.description = request.data['description']
        meeting.short_description = request.data['short_description']
        record = request.data['record']
        if record == "":
            record = False
            meeting.record = record
        else:
            meeting.record = record
        duration = request.data['duration']
        if duration == "":
            duration = 0
            meeting.duration = duration
        else:
            meeting.duration = duration
        logout_url = request.data['logout_url']
        if logout_url == "":
            logout_url = "https://video.wiki/"
            meeting.logout_url = logout_url
        else:
            meeting.logout_url = logout_url
        mute_on_start = request.data['mute_on_start']
        if mute_on_start == "":
            mute_on_start = False
            meeting.mute_on_start = mute_on_start
        else:
            meeting.mute_on_start = mute_on_start
        banner_text = request.data['banner_text']
        meeting.banner_text = banner_text
        logo = request.data['logo']
        if logo == "":
            logo = "https://class.video.wiki/images/VideoWiki_Logo.svg"
            meeting.logo = logo
        else:
            meeting.logo = logo
        end_when_no_moderator = request.data['end_when_no_moderator']
        if end_when_no_moderator =="":
            end_when_no_moderator = False
            meeting.end_when_no_moderator = end_when_no_moderator
        else:
            meeting.end_when_no_moderator = end_when_no_moderator
        guest_policy = request.data['guest_policy']
        if guest_policy == "":
            guest_policy = "ALWAYS_ACCEPT"
            meeting.guest_policy = guest_policy
        else:
            meeting.guest_policy = guest_policy
        allow_moderator_to_unmute_user = request.data['allow_moderator_to_unmute_user']
        if allow_moderator_to_unmute_user == "":
            allow_moderator_to_unmute_user = False
            meeting.allow_moderator_to_unmute_user = allow_moderator_to_unmute_user
        else:
            meeting.allow_moderator_to_unmute_user = allow_moderator_to_unmute_user
        webcam_only_for_moderator = request.data['webcam_only_for_moderator']
        if webcam_only_for_moderator == "":
            webcam_only_for_moderator = False
            meeting.webcam_only_for_moderator = webcam_only_for_moderator
        else:
            meeting.webcam_only_for_moderator = webcam_only_for_moderator
        auto_start_recording = request.data['auto_start_recording']
        if auto_start_recording == "":
            auto_start_recording = False
            meeting.auto_start_recording = auto_start_recording
        else:
            meeting.auto_start_recording = auto_start_recording
        allow_start_stop_recording = request.data['allow_start_stop_recording']
        if allow_start_stop_recording == "":
            allow_start_stop_recording =  True
            meeting.allow_start_stop_recording = allow_start_stop_recording
        else:
            meeting.allow_start_stop_recording = allow_start_stop_recording
        disable_cam = request.data['disable_cam']
        if disable_cam == "":
            disable_cam = False
            meeting.disable_cam = disable_cam
        else:
            meeting.disable_cam = disable_cam
        disable_mic = request.data['disable_mic']
        if disable_mic == "":
            disable_mic = False
            meeting.disable_mic = disable_mic
        else:
            meeting.disable_mic = disable_mic
        meeting.disable_note = False
        meeting.disable_public_chat = False
        meeting.disable_private_chat = False
        lock_layout = request.data['lock_layout']
        if lock_layout == "":
            lock_layout = False
            meeting.lock_layout = lock_layout
        else:
            meeting.lock_layout = lock_layout
        lock_on_join = request.data['lock_on_join']
        if lock_on_join == "":
            lock_on_join = True
            meeting.lock_on_join = lock_on_join
        else:
            meeting.lock_on_join = lock_on_join
        hide_users = request.data['hide_users']
        if hide_users == "":
            hide_users = False
            meeting.hide_users = hide_users
        else:
            meeting.hide_users = hide_users
        start_now = request.data['start_now']
        schedule_time = request.data['schedule_time']
        if schedule_time == "":
            start_now = "True"
        timezone = request.data['timezone']
        timezone_adder(tz=timezone)
        if start_now == "True":
            start_now = True
        elif timezone=="":
            return Response({
                "status": False,
                "message": "no timezone selected"
            }, status=status.HTTP_400_BAD_REQUEST)
        if start_now == True:
            schedule_time = datetime.datetime.now().astimezone(pytz.utc)

        meeting.raw_time = schedule_time
        if start_now != True:
            ct = tc(schedule_time,timezone)
            time_now = datetime.datetime.now().astimezone(pytz.utc)
            if time_now > ct:
                return Response({
                    "status": False,
                    "message": "invalid schedule time"},status=status.HTTP_400_BAD_REQUEST)
            meeting.schedule_time = ct
        moderators = request.data['invitee_details']
        meeting.primary_color = request.data['primary_color']
        meeting.secondary_color = request.data['secondary_color']
        meeting.back_image = request.data['back_image']
        meeting.event_tag = request.data['event_tag']
        cover_image = request.data["cover_image"]
        if cover_image != "":
            meeting.cover_image = cover_image
        else:
            cover_image = "https://api.cast.video.wiki/static/alt.png"
            meeting.cover_image = cover_image
        is_streaming = request.data["is_streaming"]
        if is_streaming == 'True':
            bool_is_streaming = True
        else:
            bool_is_streaming = False
        meeting.is_streaming = bool_is_streaming
        stream_urls_list = []
        if bool_is_streaming == True:
            bbb_resolution = "1280x720"
            meeting.bbb_resolution = bbb_resolution
            stream_urls = request.data["vw_stream_url"]
            converted_stream_urls = ast.literal_eval(stream_urls)
            if converted_stream_urls[0]["vw_stream"] == 'True':
                url = "{}{}".format(VW_RTMP_URL,meeting.public_meeting_id)
                stream_urls_list.append(url)
            if len(converted_stream_urls[1]["urls"]) > 0:
                for i in converted_stream_urls[1]["urls"]:
                    stream_urls_list.append(i)
            meeting.bbb_stream_url_vw = stream_urls_list
        give_nft = request.data["give_nft"]
        if give_nft == 'True':
            meeting.give_nft = True
        else:
            meeting.give_nft = False
        send_otp = request.data["send_otp"]
        if send_otp == 'True':
            bool_send_otp = True
        else:
            bool_send_otp = False
        meeting.send_otp = bool_send_otp
        password_auth = request.data['password_auth']
        if password_auth == 'True':
            meeting.password_auth = True
        else:
            meeting.password_auth = False
        audience_airdrop = request.data['audienceAirdrop']
        if audience_airdrop == 'True':
            meeting.audience_airdrop = True
        else:
            meeting.audience_airdrop = False
        public_otp = request.data['public_otp']
        if public_otp == 'True':
            meeting.public_otp = True
        else:
            meeting.public_otp = False
        public_stream_input = request.data["public_stream"]
        if public_stream_input == 'True':
            meeting.public_stream = True
        else:
            meeting.public_stream = False
        public_nft_flow = request.data["public_nft_flow"]
        if public_nft_flow == 'True':
            meeting.public_nft_flow = True
        else:
            meeting.public_nft_flow = False
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        if user_id == -1:
            return Response({
                'status': True,
                'message': 'User validation error'},
                status=status.HTTP_400_BAD_REQUEST
            )
        meeting.user_id = user_id
        try:
            user_name = user_info_name(token)
        except:
            user_name = meeting.event_name
        meeting.event_creator_name = user_name
        remind_schedular = meeting.public_meeting_id
        meeting.schedular_name_reminder = remind_schedular
        try:
            user_email = user_info_email(token)
        except:
            user_email = ""
        meeting.event_creator_email = user_email
        meeting.save()
        if meeting.viewer_mode == True:
            force_listen_only = request.data["listen_only_mode"]
            enable_webcam = request.data["webcam_enable"]
            enable_screen_sharing = request.data["screen_sharing"]
            ViewerDetails.objects.create(cast=meeting,
                                         force_listen_only=force_listen_only,
                                         enable_webcam=enable_webcam,
                                         enable_screen_sharing=enable_screen_sharing)
        if meeting.audience_airdrop == True:
            mint_func_name = request.data['mint_function_name']
            contract_address = request.data['contract_address']
            aib = request.data['aib']
            parameter = request.data['parameter']
            network = request.data['network']
            nft_image = request.data['nft_image']
            nft_description = request.data['nft_description']
            price = request.data['price']
            try:
                parser_o = json.loads(aib)
                if parameter != "":
                    parameter_parser = json.loads(parameter)
                else:
                    parameter_parser = ""
                NftDetails.objects.create(
                    cast=meeting,
                    mint_function_name=mint_func_name,
                    contract_address=contract_address,
                    aib=parser_o,
                    parameter=parameter_parser,
                    network=network,
                    image=nft_image,
                    description=nft_description,
                    price = price
                )
            except json.JSONDecodeError:
                Meeting.objects.filter(public_meeting_id=meeting.public_meeting_id).delete()
                return Response({
                    "message": "json error in ABI/Parameter",
                    "status": False
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass

        invite_mail(moderators, meeting.public_meeting_id)
        if start_now == True:
            url = start_cast_now(public_meeting_id=meeting.public_meeting_id, name=meeting.event_creator_name)
            msg = "cast started successfully"
        else:
            url = None
            msg = 'meeting scheduled successfully'

        if meeting.cover_image != "https://api.cast.video.wiki/static/alt.png":
            c_i = BASE_URL + "/media/" + str(meeting.cover_image)
        else:
            c_i = meeting.cover_image

        return Response({'status': True, 'event_name': meeting.event_name,
                         'meeting_id': meeting.public_meeting_id,
                         'tag': meeting.event_tag,
                         'cover_image': str(c_i),
                         'message': msg,
                         'url': url}
                        )


def timezone_adder(tz):
    dir = BASE_DIR + "/timezone_calc/timezone.txt"
    with open(dir, "a") as f:
        f.write("\n" + tz)
    f.close()

