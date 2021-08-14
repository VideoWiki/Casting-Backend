from django.utils.crypto import get_random_string
import uuid
from bbb_api.models import Meeting
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError


def generate_random_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(8, chars)
    return secret_key


def private_meeting_id_generator():
    id = str(uuid.uuid4())
    return id


def public_meeting_id_generator():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    public_meeting_id = get_random_string(3, chars) + '-' + get_random_string(3, chars) + '-' + get_random_string(3, chars)
    return public_meeting_id


def user_info(token):

    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']
        return user_id

    except ValidationError as v:
        return -1


def user_info_email(token):
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        email = valid_data['email']
        return email

    except ValidationError as v:
        return -1


