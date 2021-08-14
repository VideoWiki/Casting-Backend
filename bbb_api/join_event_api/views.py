from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info


class join_meeting(APIView):
    def post(self, request):
        name = request.data['name']
        public_meeting_id = request.data['public_meeting_id']
        password = request.data['password']
        # room_type = request.data['room_type']
        avatar_url = request.data['avatar_url']
        meeting_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
        meeting_type = meeting_obj.meeting_type
        private_meeting_id = meeting_obj.private_meeting_id
        if meeting_type == 'public':

            meeting_user_id = meeting_obj.user_id
            curr_user_id = -1
            try:
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                curr_user_id = user_info(token)
            except:
                pass

            if curr_user_id == meeting_user_id:
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.moderator_password, avatar_url)
                return Response({'status': True, 'url': result})

            if password == meeting_obj.moderator_password:
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.moderator_password, avatar_url)
                return Response({'status': True, 'url': result})

            else:  # attendee
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.attendee_password, avatar_url)
                return Response({'status': True, 'url': result})

        else: # meeting is private. password will come
            attendee_password = meeting_obj.attendee_password
            meeting_user_id = meeting_obj.user_id
            curr_user_id = -1
            try:
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                curr_user_id = user_info(token)
            except:
                pass

            if curr_user_id == meeting_user_id:
                result = Meeting.join_url(private_meeting_id, name, meeting_obj.moderator_password, avatar_url)
                return Response({'status': True, 'url': result})
            elif password == attendee_password:
                result = Meeting.join_url(private_meeting_id, name, password, avatar_url)
                return Response({'status': True, 'url': result})

            else:
                return Response({'status': False, 'url':None, 'message': 'User validation error'})