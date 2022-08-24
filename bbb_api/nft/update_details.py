from rest_framework.views import APIView, Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from ..models import Meeting, NftDetails
import json
from library.helper import user_info


class UpdateAudienceAirdrop(APIView):
    def patch(self, request):
        public_meeting_id = request.data['public_meeting_id']
        audience_airdrop = request.data['audienceAirdrop']
        public_nft_flow = request.data["public_nft_flow"]
        mint_func_name = request.data['mint_function_name']
        contract_address = request.data['contract_address']
        aib = request.data['aib']
        parameter = request.data['parameter']
        network = request.data['network']
        nft_image = request.data['nft_image']

        if type(nft_image) == str:
            nft_image = str(nft_image)
        else:
            nft_image = nft_image
        nft_description = request.data['nft_description']
        price = request.data['price']
        give_nft = request.data['give_nft']
        try:
            meeting_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
        except ObjectDoesNotExist:
            return Response({
                "message": "cast does not exist",
                "status": False
            }, status=status.HTTP_400_BAD_REQUEST)
        meeting_user_id = meeting_obj.user_id
        curr_user_id = -1
        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            curr_user_id = user_info(token)
        except:
            pass
        if curr_user_id == meeting_user_id:
            try:
                nft_obj = NftDetails.objects.get(cast=meeting_obj)
            except ObjectDoesNotExist:
                return Response({
                    "message": "nft object does not exist",
                    "status": False
                }, status=status.HTTP_400_BAD_REQUEST)

            if audience_airdrop == 'True':
                meeting_obj.audience_airdrop = True
            else:
                meeting_obj.audience_airdrop = False
            if public_nft_flow == 'True':
                meeting_obj.public_nft_flow = True
            else:
                meeting_obj.public_nft_flow = False
            if give_nft == 'True':
                meeting_obj.give_nft = True
            else:
                meeting_obj.give_nft = False
            meeting_obj.save(update_fields=['audience_airdrop','public_nft_flow','give_nft'])
            try:
                parser_o = json.loads(aib)
                if parameter != "":
                    parameter_parser = json.loads(parameter)
                else:
                    parameter_parser = ""
                nft_obj.mint_function_name = mint_func_name
                nft_obj.contract_address = contract_address
                nft_obj.aib = parser_o
                nft_obj.parameter = parameter_parser
                nft_obj.network = network
                nft_obj.image = nft_image
                nft_obj.description = nft_description
                nft_obj.price = price
                nft_obj.submitted = True
                nft_obj.save()
            except json.JSONDecodeError:
                return Response({
                    "message": "json error in ABI/Parameter",
                    "status": False
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': True, 'message': 'successful'})

        else:
            return Response({'status': False, 'message': 'user authorisation failed'},
                            status=status.HTTP_400_BAD_REQUEST)

