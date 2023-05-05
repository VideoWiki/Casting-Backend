from cast_invitee_details.models import CastInviteeDetails
from bbb_api.models import Meeting
import mandrill
from api.global_variable import MANDRILL_API_KEY, CLIENT_DOMAIN_URL
from templates.reminder1 import reminder_mod1, \
    reminder_participant, reminder_spectator, \
    reminder_viewer, reminder_viewer_otp, reminder_parti_wo_pass, \
    reminder_pri_unique
from templates.create import email_create, email_create_otp, \
    email_create_view, email_create_view_str
from templates.create2 import email_create2, email_create2_otp
from templates.create3 import email_create3
from templates.create4 import email_create4, email_create5,\
    email_create6
from base64 import b64encode
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
from icalendar import vCalAddress, vText
import json


def email_sender(public_meeting_id):
    cast_obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
    dt = cast_obj.schedule_time
    date = dt.date()
    hour = dt.hour
    min = dt.minute
    schedule_time = str(date) + " at " + str(hour) + ":" + str(min) + " GMT"
    obj = CastInviteeDetails.objects.filter(cast=cast_obj)
    meeting_url = CLIENT_DOMAIN_URL + "/e/{}/".format(cast_obj.public_meeting_id)
    send_otp = cast_obj.send_otp
    cast_type = cast_obj.meeting_type
    viewer_mode = cast_obj.viewer_mode
    for i in obj:
        email = i.email
        print(email)
        role = i.role
        event_name = cast_obj.event_name
        subject = f'Reminder for {event_name}'
        description = cast_obj.description
        print(cast_type, "ctttt")
        if cast_type == "public":
            if role == "co-host":
                meeting_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id, cast_obj.hashed_moderator_password)
                send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
            if role == "spectator":
                meeting_url = CLIENT_DOMAIN_URL + "/live/{}".format(cast_obj.public_meeting_id)
                send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
            if viewer_mode == False:
                if role == "participant":
                    print("hereeeeermmmmm")
                    meeting_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id,
                                                                       cast_obj.hashed_attendee_password)
                    send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
            if viewer_mode == True:
                if role == "viewer":
                    meeting_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id,
                                                                       cast_obj.hashed_viewer_password)
                    send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
                if role == "participant":
                    meeting_url = CLIENT_DOMAIN_URL + "/e/{}/?pass={}".format(cast_obj.public_meeting_id,
                                                                       cast_obj.hashed_attendee_password)
                    send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)

        elif cast_type == "private":
            if send_otp == True:
                if role == "spectator":
                    meeting_url = CLIENT_DOMAIN_URL + "/live/{}".format(cast_obj.public_meeting_id)
                    send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
                else:
                    meeting_url = meeting_url + f"?email={email}"
                    send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
            elif send_otp != True:
                if role == "spectator":
                    meeting_url = CLIENT_DOMAIN_URL + "/live/{}".format(cast_obj.public_meeting_id)
                    send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
                else:
                    meeting_url = meeting_url + f"?email={email}"
                    if role == "viewer":
                        send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
                    if role == "co-host":
                        meeting_url = meeting_url + f"?email={email}"
                        send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)
                    if role == "participant":
                        meeting_url = meeting_url + f"?email={email}"
                        send_remind_mail(to_email=email, subject=subject, event_name=event_name, event_url=meeting_url, event_info=description)

    return "sent"


def invite_mail(moderators, public_meeting_id):
    m_list = []
    temp = moderators[2:-2]
    p = temp.split('},{')
    for x in p:
        z = '{' + x + '}'
        j = json.loads(z)
        m_list.append(j)
    obj = Meeting.objects.get(public_meeting_id=public_meeting_id)
    for i in m_list:
        if i["give_nft"] == "True":
            bool_nft_enable = True
        else:
            bool_nft_enable = False
        cast_inv_obj = CastInviteeDetails.objects.create(cast=obj,
                                          name=i["name"],
                                          email=i["email"].lower(),
                                          role=i["type"],
                                          nft_enable=bool_nft_enable,
                                          invited= True,
                                          mint='not started'
                                          )

def send_remind_mail1( to_email, user_name, role, event_name, event_time, event_url, event_password):
    template_func = reminder_mod1(user_name, role, event_name, event_time, event_url, event_password)
    try:
        mandrill_mailer_func(template_func=template_func, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_remind_mail_spec( to_email, user_name, event_name, event_time, event_url):
    template_func = reminder_spectator(user_name, event_name, event_time, event_url)
    try:
        mandrill_mailer_func(template_func=template_func, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_remind_mail2( to_email, user_name, role, event_name, event_time, event_url, event_password):
    template_func = reminder_participant(user_name, role, event_name, event_time, event_url, event_password)
    try:
        mandrill_mailer_func(template_func=template_func, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_remind_mail_part_view( to_email, user_name, role, event_name, event_time, event_url):
    event_url = event_url + f"?email={to_email}"
    template_func = reminder_parti_wo_pass(user_name, role, event_name, event_time, event_url)
    try:
        mandrill_mailer_func(template_func=template_func, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_remind_mail_pri_unique_mail( to_email, user_name, role, event_name, event_time, event_url):
    template_func = reminder_parti_wo_pass(user_name, role, event_name, event_time, event_url)
    try:
        mandrill_mailer_func(template_func=template_func, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create1( to_email, user_name, event_name, event_time, event_url, meeting_url, moderator_password, attendee_password, pre_reg_url, start_time):

    template_func = email_create(user_name=user_name,
                                 event_name=event_name,
                                 event_time=event_time,
                                 event_url=event_url,
                                 meeting_url=meeting_url,
                                 moderator_password=moderator_password,
                                 attendee_password=attendee_password,
                                 pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name,
                              meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_create2( to_email, user_name, event_name, event_time, meeting_url, moderator_password, pre_reg_url, start_time):

    template_func = email_create2(user_name=user_name,
                                  event_name=event_name,
                                  event_time=event_time,
                                  meeting_url=meeting_url,
                                  moderator_password=moderator_password,
                                  pre_reg_url=pre_reg_url)
    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name, meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create3( to_email, user_name, event_name, event_time, meeting_url, moderator_password, attendee_password, pre_reg_url, start_time):

    template_func = email_create3(user_name=user_name,
                                  event_name=event_name,
                                  event_time=event_time,
                                 meeting_url=meeting_url,
                                  moderator_password=moderator_password,
                                  attendee_password=attendee_password,
                                  pre_reg_url=pre_reg_url)
    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name,
                              meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create4( to_email, user_name, event_name, event_time, stream_url, meeting_url, moderator_password, pre_reg_url, start_time):

    template_func = email_create4(user_name=user_name, event_name=event_name,
                                  event_time=event_time, event_url=stream_url,
                                  meeting_url=meeting_url,
                                  moderator_password=moderator_password,
                                  pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name, meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create5( to_email, user_name, event_name, event_time, stream_url, meeting_url, moderator_password, attendee_password, pre_reg_url, start_time):

    template_func = email_create5(user_name, event_name, event_time, stream_url, meeting_url, moderator_password, attendee_password, pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name, meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create6( to_email, user_name, event_name, event_time, meeting_url, moderator_password, attendee_password, pre_reg_url, start_time):

    template_func = email_create6(user_name=user_name, event_name=event_name,
                                  event_time=event_time,
                                  meeting_url=meeting_url,
                                  moderator_password=moderator_password,
                                  attendee_password=attendee_password,
                                  pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name, meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create7( to_email, user_name, event_name, event_time, meeting_url, moderator_password, attendee_password, viewer_password, pre_reg_url, start_time):

    template_func = email_create_view(user_name=user_name,
                                 event_name=event_name,
                                 event_time=event_time,
                                 meeting_url=meeting_url,
                                 moderator_password=moderator_password,
                                 attendee_password=attendee_password,
                                 viewer_password=viewer_password,
                                 pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name,
                              meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))

def send_create8( to_email, user_name, event_name, event_time, event_url, meeting_url, moderator_password, attendee_password, viewer_password, pre_reg_url, start_time):

    template_func = email_create_view_str(user_name=user_name,
                                     event_name=event_name,
                                     event_time=event_time,
                                      event_url=event_url,
                                     meeting_url=meeting_url,
                                     moderator_password=moderator_password,
                                     attendee_password=attendee_password,
                                     viewer_password=viewer_password,
                                     pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name,
                              meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create9( to_email, user_name, event_name, event_time, event_url, meeting_url, pre_reg_url, start_time):

    template_func = email_create_otp(user_name=user_name,
                                         event_name=event_name,
                                         event_time=event_time,
                                          event_url=event_url,
                                         meeting_url=meeting_url,
                                         pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name,
                              meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_create10( to_email, user_name, event_name, event_time, meeting_url, pre_reg_url, start_time):

    template_func = email_create2_otp(user_name=user_name,
                                         event_name=event_name,
                                         event_time=event_time,
                                         meeting_url=meeting_url,
                                         pre_reg_url=pre_reg_url)

    calb = icf_file_generator(start_time=start_time, event_name=event_name, to_email=to_email, user_name=user_name,
                              meeting_url=meeting_url)
    try:
        madril_mailer(template_func=template_func, calb=calb, to_email=to_email, user_name=user_name)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def icf_file_generator(start_time, event_name, to_email, user_name, meeting_url):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    event = Event()
    start_time = start_time
    duration = 1
    event.add('summary', event_name)
    event.add('dtstart', start_time)
    event.add('dtend', start_time + timedelta(hours=duration))
    # event.add('dtstamp', datetime(2022, 6, 24, 0, 0, 0, tzinfo=pytz.utc))
    organizer = vCalAddress('MAILTO:{}'.format(to_email))
    organizer.params['cn'] = vText('{}'.format(user_name))
    # organizer.params['role'] = vText('CHAIR')
    event['organizer'] = organizer
    event['location'] = vText(meeting_url)
    event.add('priority', 5)
    attendee = vCalAddress('MAILTO:{}'.format(to_email))
    attendee.params['cn'] = vText('{}'.format(user_name))
    attendee.params['ROLE'] = vText('Event Host')
    event.add('attendee', attendee, encode=0)
    cal.add_component(event)
    calb = cal.to_ical()
    return calb


def madril_mailer(template_func, calb, to_email, user_name):
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
        'subject': "Cast Registered",
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


def mandrill_mailer_func(template_func, to_email, user_name):
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
        'subject': "Reminder",
        'tags': ['password-resets'],
        'text': 'Example text content',
        'to': [{'email': to_email,
                'name': user_name,
                'type': 'to'}],
    }
    result = mandrill_client.messages.send(message=message)
    print(result[0]["status"])
    status = result[0]["status"]
    return status


mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)

def send_remind_mail(to_email, subject, event_name, event_url, event_info):
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
        'tags': ['VW_Reminder_Mail'],
        'template_name': 'VW_Reminder_Mail'
    }

    # Send the message
    result = mandrill_client.messages.send_template(template_name=message['template_name'], template_content=[], message=message)

    # Print the result
    print(result)
    return result
