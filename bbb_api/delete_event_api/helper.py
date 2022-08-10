from library.mailchimp import send_mail
from cast_invitee_details.models import CastInviteeDetails
import mandrill
from api.global_variable import MANDRILL_API_KEY
from templates.cancelled import email_format

def delete_mailer(obj):
    objs = CastInviteeDetails.objects.filter(cast=obj)
    event_name = obj.event_name
    creator_name = obj.event_creator_name
    for i in objs:
        email = i.email
        if email == None:
            pass
        else:
            event_cancelled_mail(email= email,
                                 user_name= email.split(".")[0],
                                 event_name=event_name,
                                 creator_name=creator_name)





def event_cancelled_mail(email, user_name, event_name, creator_name):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "your event has been cancelled"
    text = "Dear {}, " \
           "Your event {} was cancelled by {}. Once the presenter reschedules it, you'll be receiving a new link. " \
           "All the best, " \
           "VideoWiki team".format(user_name, event_name, creator_name)
    status_res = send_cancelled_mail(email, name, subject, user_name, event_name, creator_name)
    status = status_res
    return status


def send_cancelled_mail( to_email, name,subject, user_name, event_name, creator_name):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': email_format(user_name=user_name, event_name=event_name, creator_name=creator_name),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': subject,
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





