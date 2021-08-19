from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info
from rest_framework import status
from django_q.models import Schedule


class delete_meeting(APIView):
    def post(self, request):
        public_meeting_id = request.data['public_meeting_id']
        # password = request.data['password']
        meeting_obj = Meeting.objects.get(public_meeting_id= public_meeting_id)
        private_meeting_id = meeting_obj.private_meeting_id
        public_meeting_id = meeting_obj.public_meeting_id
        meeting_user_id = meeting_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == meeting_user_id:
            meeting_obj.delete()
            try:
                get_scheduled_object = Schedule.objects.get(name__iexact=private_meeting_id)
                get_scheduled_object.delete()
                get_remind_object = Schedule.objects.get(name__iexact=public_meeting_id)
                get_remind_object.delete()
            except:
                pass
            return Response({'status': True, 'message': 'meeting deleted successfully'})
        else:
            return Response({'status': False, 'message': 'Unable to end meeting'},
                            status=status.HTTP_400_BAD_REQUEST)