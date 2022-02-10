from rest_framework.views import APIView
from ..models import Meeting, NftDetails
from rest_framework.response import Response
from library.helper import user_info
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import BASE_URL

class FetchNftDetails(APIView):
    def get(self, request):
        try:
            cast_object = Meeting.objects.get(public_meeting_id=request.GET.get('cast_id'))
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        nft_details_object = NftDetails.objects.get(cast=cast_object)
        mint_function_name = nft_details_object.mint_function_name
        contract_adress = nft_details_object.contract_address
        aib = nft_details_object.aib
        parameter = nft_details_object.parameter
        network = nft_details_object.network
        image = nft_details_object.image
        if image == "":
            image_url = ""
        else:
            image_url = BASE_URL + image.url
        description = nft_details_object.description
        return Response({
            "status": True,
            "mint_function_name": mint_function_name,
            "contract_adress": contract_adress,
            "aib": aib,
            "parameter": parameter,
            "network": network,
            "image": image_url,
            "description": description
        })