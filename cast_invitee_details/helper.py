from api.global_variable import MANDRILL_API_KEY
import mandrill
from templates.invite_1 import email_invite1
from templates.invite_2 import email_invite2

def send_invite_mail1( to_email, name, user_name, event_name, event_time, event_url, event_password):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': email_invite1(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, event_password=event_password),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Invitation",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
        print(result[0]["status"])
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_invite_mail2( to_email, user_name, event_name, event_time, event_url, event_password, stream_url):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': email_invite2(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, stream_url= stream_url, event_password=event_password),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Invitation",
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