from cast_invitee_details.models import CastInviteeDetails
from bbb_api.models import Meeting
import mandrill
from api.global_variable import MANDRILL_API_KEY, CLIENT_DOMAIN_URL, VW_RTMP_URL
from templates.reminder2 import reminder2, reminder2_otp
from templates.reminder1 import reminder_mod1, \
    reminder_participant, reminder_spectator, \
    reminder_viewer, reminder_mod1_otp, \
    reminder_participant_otp, reminder_viewer_otp
from templates.create import email_create, email_create_otp
from templates.create2 import email_create2, email_create2_otp
from templates.create3 import email_create3, email_create3_otp
from templates.create4 import email_create4, email_create4_otp
import json, ast


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
    for i in obj:
        email = i.email
        user_name = i.name
        role = i.role
        if role == "co-host":
            password = cast_obj.moderator_password
            if cast_obj.bbb_stream_url_vw != "" and None:
                converted_stream_urls = ast.literal_eval(cast_obj.bbb_stream_url_vw)
                url = "{}{}".format(VW_RTMP_URL, cast_obj.public_meeting_id)
                if converted_stream_urls[0] == url:
                    str_url = CLIENT_DOMAIN_URL + "/live/{}".format(cast_obj.public_meeting_id)
                    send_remind_mail2(to_email=email,
                                      user_name= user_name,
                                      event_name= cast_obj.event_name,
                                      event_time= schedule_time,
                                      event_url= meeting_url,
                                      event_password= password,
                                      stream_url= str_url,
                                      send_otp= send_otp
                                      )
            else:
                send_remind_mail1(to_email=email,
                                  user_name= user_name,
                                  event_name= cast_obj.event_name,
                                  event_time= schedule_time,
                                  event_url= meeting_url,
                                  event_password= password,
                                  send_otp= send_otp)
        elif role == "participant":
            password = cast_obj.attendee_password
            send_remind_mail_participant(to_email= email,
                                         user_name= user_name,
                                         event_name= cast_obj.event_name,
                                         event_time= schedule_time,
                                         event_url= meeting_url,
                                         event_password= password,
                                         send_otp= send_otp
                                         )
        elif role == "viewer":
            password = cast_obj.viewer_password
            send_remind_mail_viewer(to_email= email,
                                    user_name= user_name,
                                    event_name= cast_obj.event_name,
                                    event_time= schedule_time,
                                    event_url= meeting_url,
                                    event_password= password,
                                    send_otp= send_otp)
        elif role == "spectator":
            if cast_obj.bbb_stream_url_vw != "":
                converted_stream_urls = ast.literal_eval(cast_obj.bbb_stream_url_vw)
                url = "{}{}".format(VW_RTMP_URL,cast_obj.public_meeting_id)
                if converted_stream_urls[0] == url:
                    str_url = CLIENT_DOMAIN_URL + "/live/{}".format(cast_obj.public_meeting_id)
                    send_remind_mail_spectator(to_email= email,
                                               user_name= user_name,
                                               event_name= cast_obj.event_name,
                                               event_time= schedule_time,
                                               event_url= str_url
                                               )

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

def send_remind_mail1( to_email, user_name, event_name, event_time, event_url, event_password, send_otp):
    if send_otp == True:
        template_func = reminder_mod1_otp(user_name=user_name,
                                          event_name=event_name,
                                          event_time=event_time,
                                          event_url=event_url)
    else:
        template_func = reminder_mod1(user_name=user_name,
                                      event_name=event_name,
                                      event_time=event_time,
                                      event_url=event_url,
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
            'subject': "Reminder",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': user_name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result[0]["status"])
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))


def send_remind_mail2( to_email, user_name, event_name, event_time, event_url, event_password, stream_url, send_otp):
    if send_otp == True:
        template_func = reminder2_otp(user_name=user_name,
                                      event_name=event_name,
                                      event_time=event_time,
                                      event_url=event_url,
                                      stream_url=stream_url)
    else:
        template_func = reminder2(user_name=user_name,
                                  event_name=event_name,
                                  event_time=event_time,
                                  event_url=event_url,
                                  event_password=event_password,
                                  stream_url=stream_url)
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


def send_remind_mail_participant( to_email, user_name, event_name, event_time, event_url, event_password, send_otp):
    if send_otp == True:
        template_func = reminder_participant_otp(user_name=user_name,
                                                 event_name=event_name,
                                                 event_time=event_time,
                                                 event_url=event_url
                                                 )
    else:
        template_func = reminder_participant(user_name=user_name,
                                             event_name=event_name,
                                             event_time=event_time,
                                             event_url=event_url,
                                             event_password=event_password
                                             )
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


def send_remind_mail_viewer( to_email, user_name, event_name, event_time, event_url, event_password, send_otp):
    if send_otp == True:
        template_func = reminder_viewer_otp(user_name=user_name,
                                            event_name=event_name,
                                            event_time=event_time,
                                            event_url=event_url
                                            )
    else:
        template_func = reminder_viewer(user_name=user_name,
                                        event_name=event_name,
                                        event_time=event_time,
                                        event_url=event_url,
                                        event_password=event_password
                                        )
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


def send_remind_mail_spectator( to_email, user_name, event_name, event_time, event_url):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': reminder_spectator(user_name=user_name,
                              event_name=event_name,
                              event_time=event_time,
                              event_url=event_url
                                       ),
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


def send_create1( to_email, user_name, event_name, event_time, event_url, meeting_url, moderator_password, attendee_password, send_otp, pre_reg_url):
    if send_otp == True:
        template_func = email_create_otp(user_name=user_name,
                                         event_name=event_name,
                                         event_time=event_time,
                                         event_url=event_url,
                                         meeting_url=meeting_url,
                                         pre_reg_url=pre_reg_url)
    else:
        template_func = email_create(user_name=user_name,
                                     event_name=event_name,
                                     event_time=event_time,
                                     event_url=event_url,
                                     meeting_url=meeting_url,
                                     moderator_password=moderator_password,
                                     attendee_password=attendee_password,
                                     pre_reg_url=pre_reg_url)

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

def send_create2( to_email, user_name, event_name, event_time, meeting_url, moderator_password, attendee_password, send_otp, pre_reg_url):
    if send_otp == True:
        template_func = email_create2_otp(user_name=user_name,
                                          event_name=event_name,
                                          event_time=event_time,
                                          meeting_url=meeting_url,
                                          pre_reg_url=pre_reg_url)
    else:
        template_func = email_create2(user_name=user_name,
                                      event_name=event_name,
                                      event_time=event_time,
                                      meeting_url=meeting_url,
                                      moderator_password=moderator_password,
                                      attendee_password=attendee_password,
                                      pre_reg_url=pre_reg_url)
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


def send_create3( to_email, user_name, event_name, event_time, nft_drop_url, meeting_url, moderator_password, attendee_password, send_otp, pre_reg_url):
    if send_otp == True:
        template_func = email_create3_otp(user_name=user_name,
                                          event_name=event_name,
                                          event_time=event_time,
                                          nft_drop_url=nft_drop_url,
                                          meeting_url=meeting_url,
                                          pre_reg_url=pre_reg_url)
    else:
        template_func = email_create3(user_name=user_name,
                                      event_name=event_name,
                                      event_time=event_time,
                                      nft_drop_url=nft_drop_url,
                                     meeting_url=meeting_url,
                                      moderator_password=moderator_password,
                                      attendee_password=attendee_password,
                                      pre_reg_url=pre_reg_url)
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


def send_create4( to_email, user_name, event_name, event_time, stream_url, nft_drop_url, meeting_url, moderator_password, attendee_password, send_otp, pre_reg_url):
    if send_otp == True:
        template_func = email_create4_otp(user_name=user_name, event_name=event_name,
                                          event_time=event_time, event_url=stream_url,
                                          nft_drop_url=nft_drop_url, meeting_url=meeting_url,
                                          pre_reg_url=pre_reg_url)
    else:
        template_func = email_create4(user_name=user_name, event_name=event_name,
                                      event_time=event_time, event_url=stream_url,
                                      nft_drop_url=nft_drop_url, meeting_url=meeting_url,
                                      moderator_password=moderator_password,
                                      attendee_password=attendee_password,
                                      pre_reg_url=pre_reg_url)
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