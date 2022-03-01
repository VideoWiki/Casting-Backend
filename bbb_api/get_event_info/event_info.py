from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from api.global_variable import BASE_URL

class meeting_info(APIView):
    def get(self, request):
        public_meeting_id = request.GET.get('public_meeting_id')
        try:
            event_object = Meeting.objects.get(public_meeting_id= public_meeting_id)
            # result = Meeting.meeting_info(private_meeting_id_object.private_meeting_id, private_meeting_id_object.moderator_password)
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
            if event_object.cover_image != "https://api.cast.video.wiki/static/alt.png":
                c_i = BASE_URL + "/media/" + str(event_object.cover_image)
            else:
                c_i = event_object.cover_image
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
                                                              "cover_image": str(c_i)
                                                              }
                             }
                            )
        except ObjectDoesNotExist:
            return Response({"status": False,
                             "message": "meeting id does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)