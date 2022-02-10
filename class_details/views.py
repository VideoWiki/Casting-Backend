from .models import ClassDetails
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class SaveClassDetails(APIView):
    def post(self, request):
        clss_id = request.data["class_id"]
        name = request.data["name"]
        email = request.data["email"]
        role = request.data["role"]
        picture = request.data["picture"]
        session = request.data["session"]

        if clss_id == "":
            return Response({
                    "status": False,
                    "message": "missing class id"
                }, status= status.HTTP_400_BAD_REQUEST)
        try:
            class_obj = ClassDetails.objects.filter(class_id=clss_id)
        except:
            pass
        if session == "NEW":
            ClassDetails.objects.filter(class_id=clss_id).delete()

        try:
            if class_obj.exists():
                for i in class_obj:
                    if email == "":
                        if i.name == name:
                            i.delete()
                        else:
                            pass
                    elif i.email == email:
                        i.delete()
        except:
            pass

        ClassDetails.objects.create(class_id=clss_id,
                                    name=name,
                                    email=email,
                                    role=role,
                                    picture=picture,
                                    session=session
                                    )
        return Response({
            "status": True,
            "message": "data saved successfully"
        })


class GetClassDetails(APIView):
    def get(self, request):
        class_id = request.GET.get("class_id")
        try:
            class_obj = ClassDetails.objects.filter(class_id=class_id)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid class id"
            })
        joinee_list = []
        if class_obj.count() != 0:
            for i in class_obj:
                name = i.name
                email = i.email
                role = i.role
                picture= i.picture
                joinee_list.append({"name": name,
                                    "email": email,
                                    "role": role,
                                    "picture": picture})
            return Response({
                "status": True,
                "data": joinee_list
            })
        else:
            return Response({
                "status": False,
                "message": "no data found"
            }, status=status.HTTP_400_BAD_REQUEST)
