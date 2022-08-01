from rest_framework.views import APIView
from ..models import Meeting, NftDetails
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from api.global_variable import BASE_URL, STREAM_URL
import django.utils.timezone
import requests
from datetime import timedelta, datetime


class meeting_info(APIView):
    def get(self, request):
        public_meeting_id = request.GET.get('public_meeting_id')
        event_object = Meeting.objects.get(public_meeting_id=public_meeting_id)
        if event_object.duration == 0:
            duration = 150
        else:
            duration = event_object.duration + 30
        events = Meeting.objects.filter(schedule_time__gt=datetime.now() + timedelta(minutes=-duration))
        if not event_object in events:
            private_meeting_id = event_object.private_meeting_id
            running = Meeting.is_meeting_running(private_meeting_id)
            if running == 'true':
                expired = False
                is_runnig = True
            else:
                expired = True
                is_runnig = False
        else:
            running = Meeting.is_meeting_running(event_object.private_meeting_id)
            expired = False
            if running == 'true':
                is_runnig = True
            else:
                is_runnig = False
        try:
            event_name = event_object.event_name
            event_creator_name = event_object.event_creator_name
            public_meeting_id = event_object.public_meeting_id
            description = event_object.description
            short_description = event_object.short_description
            event_day = event_object.schedule_time.date()
            event_time = event_object.schedule_time.time()
            send_otp = event_object.send_otp
            give_nft = event_object.give_nft
            password_auth = event_object.password_auth
            public_otp = event_object.public_otp
            public_stream = event_object.public_stream
            public_nft_status = event_object.public_nft_activate
            pub_nft_flow = event_object.public_nft_flow
            streaming_urls = event_object.bbb_stream_url_vw
            airdrop = event_object.audience_airdrop
            viewer_mode = event_object.viewer_mode
            if event_object.cover_image != "https://api.cast.video.wiki/static/alt.png":
                c_i = BASE_URL + "/media/" + str(event_object.cover_image)
            else:
                c_i = event_object.cover_image
            try:
                email = event_object.event_creator_email
            except:
                email = ""
            # url_status = "{}status".format(STREAM_URL)
            # payload = {'meeting_id': str(event_object.private_meeting_id)}
            # files = []
            # headers = {}
            # response1 = requests.request("POST", url_status, headers=headers, data=payload, files=files)
            # sp = response1.text.split(":")
            # sp2 = sp[1].split(",")
            # if sp2[0] == 'true':
            #     stream_status = True
            # else:
            #     stream_status = False
            try:
                nft_object_submitted = NftDetails.objects.get(cast=event_object).submitted
            except ObjectDoesNotExist:
                nft_object_submitted = False
            result = Meeting.get_recordings(event_object.private_meeting_id)
            if result == None:
                recording_available = False
            else:
                recording_available = True
            return Response({'status': True, 'meeting_info': {"event_name": event_name,
                                                              "event_creator_name": event_creator_name,
                                                              "public_meeting_id": public_meeting_id,
                                                              "description": description,
                                                              "short_description": short_description,
                                                              "date": event_day,
                                                              "time": event_time,
                                                              "send_otp": send_otp,
                                                              "give_nft": give_nft,
                                                              "password_auth": password_auth,
                                                              "public_otp": public_otp,
                                                              "public_stream": public_stream,
                                                              "public_nft_status": public_nft_status,
                                                              "pub_nft_flow": pub_nft_flow,
                                                              "cover_image": str(c_i),
                                                              "stream_urls": streaming_urls,
                                                              "airdrop": airdrop,
                                                              "expired": expired,
                                                              "running": is_runnig,
                                                              "viewer_mode": viewer_mode,
                                                              "stream_status": False,
                                                              "nft_details_submitted": nft_object_submitted,
                                                              "event_creator_email": email,
                                                              "recording_available": recording_available
                                                              }
                             }
                            )
        except ObjectDoesNotExist:
            return Response({"status": False,
                             "message": "meeting id does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)