from rest_framework.views import APIView
from ..models import Meeting, NftDetails
from rest_framework.response import Response
from library.helper import user_info
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from api.global_variable import BASE_URL

class FetchNftDetails(APIView):
    def get(self, request):
        nft_method = request.GET.get("nft_type")
        try:
            cast_object = Meeting.objects.get(public_meeting_id=request.GET.get('cast_id'))
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid cast_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        if nft_method == "vc":
            nft_details_object = NftDetails.objects.get(cast=cast_object, nft_type="vc")
            mint_function_name = nft_details_object.mint_function_name
            contract_adress = nft_details_object.contract_address
            aib = nft_details_object.aib
            parameter = nft_details_object.parameter
            network = nft_details_object.network
            image = nft_details_object.image
            nft_activated = cast_object.public_nft_activate
            pub_nft_flow = cast_object.public_nft_flow
            price = nft_details_object.price
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
                "description": description,
                "price": price,
                "nft_activated": nft_activated,
                "pub_nft_flow": pub_nft_flow
            })
        else:
            nft_details_object = NftDetails.objects.get(cast=cast_object, nft_type="simple")
            mint_function_name = nft_details_object.mint_function_name
            contract_adress = nft_details_object.contract_address
            aib = nft_details_object.aib
            parameter = nft_details_object.parameter
            network = nft_details_object.network
            image = nft_details_object.image
            nft_activated = cast_object.public_nft_activate
            pub_nft_flow = cast_object.public_nft_flow
            price = nft_details_object.price
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
                "description": description,
                "price": price,
                "nft_activated": nft_activated,
                "pub_nft_flow": pub_nft_flow
            })