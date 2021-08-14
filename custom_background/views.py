from rest_framework.views import APIView
from rest_framework.response import Response
from .models import background_pictures
# Create your views here.


class photo_api(APIView):
    def get(self, request):

        if request.GET.get("category")=="all":
            background_picture_object = background_pictures.objects.all().order_by('id')
            bg_images_list = []
            for i in background_picture_object:
                picture_details = {
                    "id": i.id,
                    "title": i.name,
                    "category": i.category,
                    "url": i.picture_url
                }
                bg_images_list.append(picture_details)
            return Response({"message": "successful", 'status': True, "data": bg_images_list})
        else:
            bg_images_list = []
            photos = background_pictures.objects.filter(
                category=request.GET.get("category")).order_by("id")
            for i in photos:
                picture_details = {
                    "id": i.id,
                    "title": i.name,
                    "category": i.category,
                    "url": i.picture_url
                }
                bg_images_list.append(picture_details)
            return Response({"message": "successful", 'status': True, "data": bg_images_list})





