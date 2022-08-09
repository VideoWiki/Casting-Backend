from rest_framework.views import APIView
from ..models import Meeting, MailTemplateDetails
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.core.exceptions import ObjectDoesNotExist
from bbb_api.create_event_api.helper import icf_file_generator
import mandrill
from api.global_variable import CLIENT_DOMAIN_URL
from bbb_api.create_event_email_sender import madril_mailer


class SendTestMail(APIView):
    def post(self, request):
        cast_id = request.data['cast_id']
        role = request.data['role']
        if cast_id == "":
            return Response({
                "message": "invalid cast id",
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
        try:
            cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        except ObjectDoesNotExist:
            return Response({
                "message": "invalid cast id",
                "status": False
            },status=HTTP_400_BAD_REQUEST)

        cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        if role == 'co-host':
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            meet_url = CLIENT_DOMAIN_URL + "/{}/?pass={}".format(cast_id, cast_obj.hashed_moderator_password)
        elif role == "participant":
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            meet_url = CLIENT_DOMAIN_URL + "/{}/?pass={}".format(cast_id, cast_obj.hashed_attendee_password)
        if cast_obj.viewer_mode == True and role == "viewer":
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            meet_url = CLIENT_DOMAIN_URL + "/{}/?pass={}".format(cast_id, cast_obj.hashed_viewer_password)
        calb = icf_file_generator(start_time=cast_obj.schedule_time, event_name=cast_obj.event_name,
                                  to_email=cast_obj.event_creator_email, user_name=cast_obj.event_creator_name,
                                  meeting_url=meet_url)
        try:
            madril_mailer(template_func=temp_obj.body, subject=temp_obj.subject, calb=calb,
                          to_email=cast_obj.event_creator_email,
                          user_name=cast_obj.event_creator_name)
            status = HTTP_200_OK
            message = "test mail sent successfully"
        except mandrill.Error as e:
            status = HTTP_400_BAD_REQUEST
            message = "failed to send test mail"
            print("An exception occurred: {}".format(e))


        return Response({
            "status": status,
            "message": message
        })