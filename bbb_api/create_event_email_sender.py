from datetime import datetime, timedelta
from cast_invitee_details.helper import send_invite_mail_spec, send_invite_mail_otp, \
    send_invite_mail_pass
from bbb_api.create_event_api.helper import icf_file_generator
from .models import MailTemplateDetails, Meeting
from bbb_api.create_event_api.helper import send_create1, send_create2, send_create3,\
    send_create4, send_create6, send_create5, send_create7, send_create8,\
    send_create9, send_create10
import pytz, mandrill
from base64 import b64encode
from api.global_variable import MANDRILL_API_KEY, CLIENT_DOMAIN_URL

mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)

def event_registration_mail(email, event_name, date, time,
                            pre_reg_url):
    subject = f'Cast Registered - {event_name}'
    registration_mail(to_email=email, subject=subject, event_name=event_name, date=date, time=time, event_url=pre_reg_url)


def attendee_mail(email, event_name, event_time, event_url, event_password,
                  co_password, stream_url, role, send_otp, cast_type, dt, creator_nmae,
                  creator_email, viewer_mode, public_otp, viewer_pass, cast_id, date, description):
    if cast_type == "public":
        cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        if role == 'co-host':
            meet_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_id, cast_obj.hashed_moderator_password)
            send_invite_mail(subject=f'Invitation to {event_name}', to_email=email, event_name=event_name,
                             date=date, time=event_time, event_url=meet_url, event_info=description)
        if role == "participant":
            meet_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_id, cast_obj.hashed_attendee_password)
            send_invite_mail(subject=f'Invitation to {event_name}', to_email=email, event_name=event_name,
                             date=date, time=event_time, event_url=meet_url, event_info=description)

        if cast_obj.viewer_mode == True and role == "viewer":
            meet_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_id, cast_obj.hashed_viewer_password)
            send_invite_mail(subject=f'Invitation to {event_name}', to_email=email, event_name=event_name,
                             date=date, time=event_time, event_url=meet_url, event_info=description)

        if cast_obj.is_streaming == True and role == 'spectator':
            send_spectator_mail(to_email=email, subject=f'Invitation to {event_name}', event_name=event_name,
                                date=date, time=event_time, event_url=stream_url, event_info=description)

    elif cast_type == "private":
        if send_otp == True:
            if role == "co-host":
                event_url = event_url + "?email={}".format(email)
                send_invite_mail(subject=f'Invitation to {event_name}', to_email=email, event_name=event_name,
                                 date=date, time=event_time, event_url=event_url, event_info=description)
            elif role == "participant":
                event_url = event_url + "?email={}".format(email)
                send_invite_mail(subject=f'Invitation to {event_name}', to_email=email, event_name=event_name,
                                 date=date, time=event_time, event_url=event_url, event_info=description)

            elif role == "viewer":
                event_url = event_url + "?email={}".format(email)
                send_invite_mail(subject=f'Invitation to {event_name}', to_email=email, event_name=event_name,
                                 date=date, time=event_time, event_url=event_url, event_info=description)

            elif role == "spectator":
                send_spectator_mail(to_email=email, subject=f'Invitation to {event_name}', event_name=event_name,
                                    date=date, time=event_time, event_url=stream_url, event_info=description)













def madril_mailer(template_func, subject, calb, to_email, user_name):
    mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
    message = {
        'html': template_func,
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
        'attachments': [{'type': "text/calendar",
                         'content': b64encode(calb).decode('utf-8'),
                         'name': "calendar.ics",
                         }],
        'to': [{'email': to_email,
                'name': user_name,
                'type': 'to'}],
    }
    result = mandrill_client.messages.send(message=message)
    print(result)
    status = result[0]["status"]
    return status

def time_subtractor(time_string):
    h = time_string.hour
    if len(str(h))==1:
        h = "0{}".format(str(h))
    m = time_string.minute
    if len(str(m)) == 1:
        m = "0{}".format(str(m))
    s1 = '00:10:00'
    s2 = '{}:{}:00'.format(str(h), str(m))
    format = '%H:%M:%S'
    subtracted_time = datetime.strptime(s2, format) - datetime.strptime(s1, format)
    return subtracted_time

def time_subtractor2(time):
    s1 = '00:00:30'
    s2 = '{}:{}:00'.format(time[11:13], time[14:16])
    format = '%H:%M:%S'
    subtracted_time = datetime.strptime(s2, format) - datetime.strptime(s1, format)
    return subtracted_time

def time_convertor(time):
    tim = time
    ds = tim[:33]
    datetime_object = datetime.strptime(ds, '%a %b %d %Y %H:%M:%S %Z%z').strftime("%Y-%m-%d %H:%M:%S")
    a = tim.split(' ')
    b = a[5]
    c = b[3:]
    year = datetime_object[:4]
    mon = datetime_object[5:7]
    day = datetime_object[8:10]
    if c[0] == "+":
        d = c[1:]
        hour = datetime_object[11:13]
        min = datetime_object[14:16]
        original_time = datetime(year=int(year), month=int(mon), day=int(day)) + timedelta(hours=int(hour),
                                                                                           minutes=int(min))
        f_time = original_time - timedelta(hours=int(d[:2]), minutes=int(d[2:])) - timedelta(hours=int(d[:2]), minutes=int(d[2:]))
    if c[0] == "-":
        d = c[1:]
        hour = datetime_object[11:13]
        min = datetime_object[14:16]
        original_time = datetime(year=int(year), month=int(mon), day=int(day)) + timedelta(hours=int(hour),
                                                                                           minutes=int(min))
        f_time = original_time + timedelta(hours=int(d[:2]), minutes=int(d[2:])) + timedelta(hours=int(d[:2]), minutes=int(d[2:]))
    return f_time


def tc(time, tz1):
    local = pytz.timezone(tz1)
    naive = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def registration_mail(to_email, subject, event_name, date, time, event_url):
    message = {
        'from_email': 'support@videowiki.pt',
        'from_name': 'VideoWiki',
        'to': [{'email': to_email, 'type': 'to'}],
        'subject': subject,
        'merge_language': 'mailchimp',
        'merge_vars': [
            {
                'rcpt': to_email,
                'vars': [

                    {
                        'name': 'user',
                        'content': to_email
                    },
                    {
                        'name': 'cast_name',
                        'content': event_name
                    },
                    {
                        'name': 'date',
                        'content': date
                    },
                    {
                        'name': 'time',
                        'content': time
                    },
                    {
                        'name': 'pre_reg_url',
                        'content': event_url
                    },
                    {
                        'name': 'mail',
                        'content': 'support@videowiki.pt'
                    }
                ]
            }
        ],
        'tags': ['VW-Cast-Registration'],
        'template_name': 'VW-Cast-Registration'
    }

    # Send the message
    result = mandrill_client.messages.send_template(template_name=message['template_name'], template_content=[], message=message)

    # Print the result
    print(result)
    return result


def send_invite_mail(to_email, subject, event_name, date, time, event_url, event_info):
    message = {
        'from_email': 'support@videowiki.pt',
        'from_name': 'VideoWiki',
        'to': [{'email': to_email, 'type': 'to'}],
        'subject': subject,
        'merge_language': 'mailchimp',
        'merge_vars': [
            {
                'rcpt': to_email,
                'vars': [
                    {
                        'name': 'recipient_name',
                        'content': to_email
                    },
                    {
                        'name': 'event_name',
                        'content': event_name
                    },
                    {
                        'name': 'date',
                        'content': str(date)
                    },
                    {
                        'name': 'time',
                        'content': str(time)
                    },
                    {
                        'name': 'event_url',
                        'content': event_url
                    },
                    {
                        'name': 'event_info',
                        'content': event_info
                    },
                    {
                        'name': 'mail',
                        'content': 'support@videowiki.pt'
                    }
                ]
            }
        ],
        'tags': ['CAST_INVITATION_MAIL'],
        'template_name': 'NEW_INVITING_MAIL'
    }

    # Send the message
    result = mandrill_client.messages.send_template(template_name=message['template_name'], template_content=[], message=message)

    # Print the result
    print(result)
    return result

def send_spectator_mail(to_email, subject, event_name, date, time, event_url, event_info):
    message = {
        'from_email': 'support@videowiki.pt',
        'from_name': 'VideoWiki',
        'to': [{'email': to_email, 'type': 'to'}],
        'subject': subject,
        'merge_language': 'mailchimp',
        'merge_vars': [
            {
                'rcpt': to_email,
                'vars': [
                    {
                        'name': 'recipient_name',
                        'content': to_email
                    },
                    {
                        'name': 'event_name',
                        'content': event_name
                    },
                    {
                        'name': 'date',
                        'content': str(date)
                    },
                    {
                        'name': 'time',
                        'content': str(time)
                    },
                    {
                        'name': 'event_url',
                        'content': event_url
                    },
                    {
                        'name': 'event_info',
                        'content': event_info
                    },
                    {
                        'name': 'mail',
                        'content': 'support@videowiki.pt'
                    }
                ]
            }
        ],
        'tags': ['invitation'],
        'template_name': 'NEW_INVITE_FOR_SPECTATOR'
    }

    # Send the message
    result = mandrill_client.messages.send_template(template_name=message['template_name'], template_content=[], message=message)

    # Print the result
    print(result)
    return result
