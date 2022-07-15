from rest_framework.views import APIView
from ..models import Meeting, MailTemplateDetails
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.core.exceptions import ObjectDoesNotExist


class GetTemplate(APIView):
    def get(self, request):
        cast_id = request.GET.get('cast_id')
        role = request.GET.get('role')
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
        temp = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
        data = {
            "subject": temp.subject,
            "role": temp.role,
            "body": temp.body
        }



        return Response({
            "status": True,
            "data": data
        })