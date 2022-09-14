from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta, datetime
from api.global_variable import BASE_URL
from .textAdder import ImageWriter
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import FileResponse


class textAdderView(APIView):
    def get(self, request):
        user_name = request.GET.get("user_name")
        if user_name == "":
            return Response({
                "status": False,
                "message": "username field can not be empty"
            }, status=HTTP_400_BAD_REQUEST)
        image_url = ImageWriter(user_name=user_name)
        # return Response({"status": True,
        #                  "image_url": image_url
        #                  })
        response = FileResponse(open(image_url, 'rb'))
        return response