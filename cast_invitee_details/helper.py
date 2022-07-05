from api.global_variable import MANDRILL_API_KEY
import mandrill
from templates.invite_1 import email_invite1_mod, email_invite_participant, \
    email_invite_viewer, email_invite_spectator, email_invite1_mod_otp, \
    email_invite_participant_otp, email_invite_viewer_otp, \
    email_invite_participant_vm, email_invite_viewer_pub, \
    email_invite_spec, email_invite1_otp, email_invite1_pass
from templates.invite_2 import email_invite2, email_invite2_otp
from base64 import b64encode
import icalendar
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import pytz
from icalendar import vCalAddress, vText
from icalendar import vDatetime
import json

def send_invite_mail1( to_email, user_name, event_name, event_time, event_url, event_password, send_otp):
    if send_otp == True:
        template_func = email_invite1_mod_otp(user_name=user_name, event_name=event_name, event_time=event_time,
                                              event_url=event_url)
    else:
        template_func = email_invite1_mod(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url,
                          event_password=event_password)
    try:
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

def send_invite_mail2( to_email, user_name, event_name, event_time, event_url, event_password, stream_url, send_otp):
    if send_otp == True:
        template_func = email_invite2_otp(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, stream_url= stream_url)
    else:
        template_func = email_invite2(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, stream_url= stream_url, event_password=event_password)
    try:
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

def send_invite_mail3( to_email, user_name, event_name, event_time, stream_url):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': email_invite_spectator(user_name=user_name, event_name=event_name, event_time=event_time, stream_url= stream_url),
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


def send_invite_mail4( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role):

    template_func = email_invite_participant(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url)

    calb = generate_cal(dt, event_name, creator_email, creator_nmae, event_url, to_email, user_name, role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_invite_mail_cohost( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role, password):

    template_func = email_invite1_mod(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, event_password=password)
    print(dt, event_name, creator_email, creator_nmae, event_url, to_email, user_name, role)
    calb = generate_cal(dt=dt, event_name=event_name, creator_email=creator_email,
                        creator_nmae=creator_nmae, event_url=event_url, to_email=to_email, user_name=user_name, role=role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_invite_mail_part_vm( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role, password):

    template_func = email_invite_participant_vm(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, password=password)
    print(dt, event_name, creator_email, creator_nmae, event_url, to_email, user_name, role)
    calb = generate_cal(dt=dt, event_name=event_name, creator_email=creator_email,
                        creator_nmae=creator_nmae, event_url=event_url, to_email=to_email, user_name=user_name, role=role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_invite_mail_viewer( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role):

    template_func = email_invite_viewer_pub(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url)
    print(dt, event_name, creator_email, creator_nmae, event_url, to_email, user_name, role)
    calb = generate_cal(dt=dt, event_name=event_name, creator_email=creator_email,
                        creator_nmae=creator_nmae, event_url=event_url, to_email=to_email, user_name=user_name, role=role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_invite_mail_spec( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role):

    template_func = email_invite_spec(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url)
    print(dt, event_name, creator_email, creator_nmae, event_url, to_email, user_name, role)
    calb = generate_cal(dt=dt, event_name=event_name, creator_email=creator_email,
                        creator_nmae=creator_nmae, event_url=event_url, to_email=to_email, user_name=user_name, role=role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_invite_mail_otp( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role):

    template_func = email_invite1_otp(user_name=user_name, event_name=event_name, event_time=event_time, role=role, event_url=event_url)
    calb = generate_cal(dt=dt, event_name=event_name, creator_email=creator_email,
                        creator_nmae=creator_nmae, event_url=event_url, to_email=to_email, user_name=user_name, role=role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_invite_mail_pass( user_name, to_email, event_name, event_time, event_url, dt, creator_nmae, creator_email, role, password):

    template_func = email_invite1_pass(user_name=user_name, event_name=event_name, event_time=event_time, role=role, event_url=event_url, password=password)
    calb = generate_cal(dt=dt, event_name=event_name, creator_email=creator_email,
                        creator_nmae=creator_nmae, event_url=event_url, to_email=to_email, user_name=user_name, role=role)
    try:
        mandrill_sender(template_func, calb, to_email, user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_invite_mail5( to_email, user_name, event_name, event_time, event_url, event_password, send_otp):
    if send_otp == True:
        template_func = email_invite_viewer_otp(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url)
    else:
        template_func = email_invite_viewer(user_name=user_name, event_name=event_name, event_time=event_time, event_url=event_url, event_password=event_password)
    try:
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


def send_otp_details(email, otp):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name,
        }

    ]
    subject = otp
    status = send_otp_mail(email, name, subject, global_merge_vars, otp)
    return status

def send_otp_mail( to_email, name,subject, global_merge_vars, otp):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "OTP",
            'tags': ['password-resets'],
            'text': str(otp),
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message=message)
        print(result)
        status = result[0]['status']
        return status
    except mandrill.Error as e:
        status = 'A mandrill error occurred:'
        print('A mandrill error occurred:')
        return status


def generate_cal(dt, event_name, creator_email, creator_nmae, event_url, to_email, user_name, role):
    print(creator_nmae + "ce", creator_email)
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    event = Event()
    start_time = dt
    print(start_time)
    duration = 1
    event.add('summary', event_name)
    event.add('dtstart', start_time)
    event.add('dtend', start_time + timedelta(hours=duration))
    event.add('dtstamp', datetime(2022, 6, 24, 0, 0, 0, tzinfo=pytz.utc))
    organizer = vCalAddress('MAILTO:{}'.format(creator_nmae))
    organizer.params['cn'] = vText('{}'.format(creator_email))
    event['organizer'] = organizer
    event['location'] = vText(event_url)
    event.add('priority', 5)
    attendee = vCalAddress('MAILTO:{}'.format(to_email))
    attendee.params['cn'] = vText('{}'.format(creator_nmae))
    attendee.params['ROLE'] = vText(role)
    event.add('attendee', attendee, encode=0)
    cal.add_component(event)
    calb = cal.to_ical()
    return calb


def mandrill_sender(template_func, calb, to_email, user_name):
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
        'subject': "Invitation",
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
    print(result[0]["status"])
    status = result[0]["status"]
    return status