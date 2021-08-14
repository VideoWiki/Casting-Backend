from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response
from library.helper import user_info


class user_recordings(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_id = user_info(str(token))
        a = Meeting.objects.filter(user_id=user_id)
        b = a.all()
        c = b.filter().values("private_meeting_id")
        d = []
        l = list(c)
        for i in l:
            c = i["private_meeting_id"]
            d.append(c)
        fl = []
        for i in d:
            result = Meeting.get_recordings(i)
            if result!= None:
                fl.append(result)
        return Response({"status": fl})