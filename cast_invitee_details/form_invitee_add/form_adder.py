import requests
import json
from bbb_api.models import Meeting
from ..models import CastInviteeDetails
from django.core.exceptions import ObjectDoesNotExist
import logging
logger = logging.getLogger('__name__')
logger_1 = logging.getLogger('django')
from api.global_variable import TYPEFORM_URL


def form_adder():
    url = TYPEFORM_URL

    payload = {}
    headers = {
        'Authorization': 'Bearer tfp_7SG5imHPseNuk5wT8CmQUC2CMvpdH3K5mAGh8TZ7GbFm_3pf2RmQVryrcEK'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    decoded_response = json.loads(response.content.decode())
    for i in decoded_response['items']:
        hidden = i['hidden']
        creater_email = hidden['creater_email']
        event_name = hidden['event_name']
        user_name = i['answers'][0]['text']
        email = i['answers'][1]['email']
        try:
            cast_obj = Meeting.objects.get(event_creator_email=creater_email, event_name=event_name)
            print(cast_obj)
            if CastInviteeDetails.objects.filter(email=email, name=user_name, cast=cast_obj).exists():
                pass
            else:
                CastInviteeDetails.objects.create(cast=cast_obj, name=user_name, email=email, role='participant')
        except ObjectDoesNotExist:
            logger_1.warning(creater_email, event_name, user_name, email)
