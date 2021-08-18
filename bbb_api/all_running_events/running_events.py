from rest_framework.views import APIView
from ..models import Meeting
from rest_framework.response import Response


class meetings(APIView):
    def get(self, request):
        print("here")
        meetings = Meeting.get_meetings()
        return Response({'status': True, 'meetings': meetings})