from cast_invitee_details.models import CastInviteeDetails
from bbb_api.models import Meeting
import mandrill
from api.global_variable import MANDRILL_API_KEY, CLIENT_DOMAIN_URL
from templates.reminder2 import reminder2
from templates.reminder1 import reminder1
from templates.create import email_create
from templates.create2 import email_create2

def email_sender(name):
    cast_obj = Meeting.objects.get(event_name=name)
    dt = cast_obj.schedule_time
    date = dt.date()
    hour = dt.hour
    min = dt.minute
    schedule_time = str(date) + " at " + str(hour) + ":" + str(min) + " GMT"
    print(schedule_time)
    obj = CastInviteeDetails.objects.filter(cast=cast_obj)
    meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(cast_obj.public_meeting_id)
    for i in obj:
        email = i.email
        user_name = i.name
        role = i.role
        if role == "attendee":
            password = cast_obj.attendee_password
        else:
            password = cast_obj.moderator_password
        send_remind_mail1(email, user_name=user_name, event_name=cast_obj.event_name, event_time=cast_obj.schedule_time, event_url=meeting_url, event_password=password)
    return "sent"


def invite_mail(moderators, meeting_name):
    obj = Meeting.objects.get(event_name=meeting_name)
    for i in moderators:
        CastInviteeDetails.objects.create(cast=obj, name=i["name"], email=i["email"], role=i["type"])

def send_remind_mail1( to_email, user_name, event_name, event_time, event_url, event_password):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': reminder1(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, event_password=event_password),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Reminder",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': user_name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
        print(result[0]["status"])
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_remind_mail2( to_email, user_name, event_name, event_time, event_url, event_password):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': reminder2(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, event_password=event_password),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Reminder",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': user_name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
        print(result[0]["status"])
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create1( to_email, user_name, event_name, event_time, event_url, meeting_url, moderator_password, attendee_password):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': email_create(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url,
                                 meeting_url=meeting_url, moderator_password=moderator_password, attendee_password=attendee_password),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Cast Registered",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': user_name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_create2( to_email, user_name, event_name, event_time, meeting_url, moderator_password, attendee_password):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': email_create2(user_name=user_name, event_name=event_name, event_time=event_time,
                                  meeting_url=meeting_url, moderator_password=moderator_password, attendee_password=attendee_password),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Cast Registered",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': user_name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

