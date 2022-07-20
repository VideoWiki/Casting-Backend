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

def event_registration_mail(email, user_name, event_name, time, stream_url, meeting_url,
                            nft_drop_url, moderator_password, attendee_password, send_otp,
                            pre_reg_url, start_time, event_type, viewer_mode, viewer_password):
    if event_type == "public":
        if stream_url == "" and viewer_mode == False:
            send_create2(email, user_name, event_name,
                         time, meeting_url, moderator_password,
                         pre_reg_url, start_time)
        elif stream_url == "" and viewer_mode == True:
            send_create6(email, user_name, event_name, time,
                         meeting_url, moderator_password, attendee_password,
                         pre_reg_url, start_time)
        elif stream_url != "" and viewer_mode == False:
            send_create4(email, user_name, event_name, time,
                         stream_url, meeting_url, moderator_password,
                         pre_reg_url, start_time)
        elif stream_url != "" and viewer_mode == True:
            send_create5(email, user_name, event_name, time, stream_url,
                         meeting_url, moderator_password, attendee_password,
                         pre_reg_url, start_time)

    elif event_type == "private":
        if send_otp == False and stream_url == "" and viewer_mode == False:
            send_create3(email, user_name, event_name,
                         time, meeting_url, moderator_password,
                         attendee_password, pre_reg_url, start_time)
        elif send_otp == False and stream_url != "" and viewer_mode == False:
            send_create1(email, user_name, event_name, time, stream_url, meeting_url, moderator_password,
                         attendee_password, pre_reg_url, start_time)
        elif send_otp == False and stream_url == "" and viewer_mode == True:
            send_create7(email, user_name, event_name, time, meeting_url, moderator_password,
                         attendee_password, viewer_password, pre_reg_url, start_time)
        elif send_otp == False and stream_url != "" and viewer_mode == True:
            send_create8(email, user_name, event_name,
                         time, stream_url, meeting_url, moderator_password,
                         attendee_password, viewer_password,
                         pre_reg_url, start_time)
        elif send_otp == True and stream_url =="":
            send_create10(email, user_name, event_name, time, meeting_url, pre_reg_url, start_time)
        elif send_otp == True and stream_url !="":
            send_create9(email, user_name, event_name, time, stream_url, meeting_url, pre_reg_url, start_time)







def attendee_mail(user_name, email, event_name, event_time, event_url, event_password,
                  co_password, stream_url, role, send_otp, cast_type, dt, creator_nmae,
                  creator_email, viewer_mode, public_otp, viewer_pass, cast_id):
    if cast_type == "public":
        print("sss", event_time)
        cast_obj = Meeting.objects.get(public_meeting_id=cast_id)
        if role == 'co-host':
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            meet_url = CLIENT_DOMAIN_URL + "/{}/?pass={}".format(cast_id, cast_obj.hashed_moderator_password)
            calb = icf_file_generator(start_time=dt, event_name=event_name, to_email=email, user_name=user_name, meeting_url=meet_url)
            try:
                madril_mailer(template_func=temp_obj.body, subject= temp_obj.subject, calb=calb, to_email=email, user_name=user_name)
            except mandrill.Error as e:
                print("An exception occurred: {}".format(e))
        if role == "participant":
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            meet_url = CLIENT_DOMAIN_URL + "/{}/?pass={}".format(cast_id, cast_obj.hashed_attendee_password)
            calb = icf_file_generator(start_time=dt, event_name=event_name, to_email=email, user_name=user_name,
                                      meeting_url=meet_url)
            try:
                madril_mailer(template_func=temp_obj.body, subject=temp_obj.subject, calb=calb, to_email=email,
                              user_name=user_name)
            except mandrill.Error as e:
                print("An exception occurred: {}".format(e))
        if cast_obj.viewer_mode == True and role == "viewer":
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            meet_url = CLIENT_DOMAIN_URL + "/{}/?pass={}".format(cast_id, cast_obj.hashed_viewer_password)
            calb = icf_file_generator(start_time=dt, event_name=event_name, to_email=email, user_name=user_name,
                                      meeting_url=meet_url)
            try:
                madril_mailer(template_func=temp_obj.body, subject=temp_obj.subject, calb=calb, to_email=email,
                              user_name=user_name)
            except mandrill.Error as e:
                print("An exception occurred: {}".format(e))
        if cast_obj.is_streaming == True:
            temp_obj = MailTemplateDetails.objects.get(cast=cast_obj, role=role)
            calb = icf_file_generator(start_time=event_time, event_name=event_name, to_email=email, user_name=user_name,
                                      meeting_url=stream_url)
            try:
                madril_mailer(template_func=temp_obj.body, subject=temp_obj.subject, calb=calb, to_email=email,
                              user_name=user_name)
            except mandrill.Error as e:
                print("An exception occurred: {}".format(e))


    elif cast_type == "private":
        if send_otp == True:
            if role == "co-host":
                send_invite_mail_otp(user_name=user_name, event_name=event_name, event_time=event_time, role=role,
                                     event_url=event_url, to_email=email, dt=dt, creator_email=creator_email,
                                     creator_nmae=creator_nmae)
            elif role == "participant":
                send_invite_mail_otp(user_name=user_name, event_name=event_name, event_time=event_time, role=role,
                                     event_url=event_url, to_email=email, dt=dt, creator_email=creator_email,
                                     creator_nmae=creator_nmae)
            elif role == "viewer":
                send_invite_mail_otp(user_name=user_name, event_name=event_name, event_time=event_time, role=role,
                                     event_url=event_url, to_email=email, dt=dt, creator_email=creator_email,
                                     creator_nmae=creator_nmae)
            elif role == "spectator":
                send_invite_mail_spec(user_name, email, event_name, event_time, stream_url, dt, creator_nmae,
                                      creator_email, role)
        elif send_otp == False and public_otp == True:
            if role == "co-host":
                send_invite_mail_pass(user_name=user_name, event_name=event_name, event_time=event_time, role=role,
                                     event_url=event_url, to_email=email, dt=dt, creator_email=creator_email,
                                      creator_nmae=creator_nmae, password= co_password)
            elif role == "participant":
                send_invite_mail_pass(user_name=user_name, event_name=event_name, event_time=event_time, role=role,
                                     event_url=event_url, to_email=email, dt=dt, creator_email=creator_email,
                                     creator_nmae=creator_nmae, password=event_password)
            elif role == "viewer" and viewer_mode == True:
                send_invite_mail_pass(user_name=user_name, event_name=event_name, event_time=event_time, role=role,
                                     event_url=event_url, to_email=email, dt=dt, creator_email=creator_email,
                                     creator_nmae=creator_nmae, password= viewer_pass)
            elif role == "spectator":
                send_invite_mail_spec(user_name, email, event_name, event_time, stream_url, dt, creator_nmae,
                                      creator_email, role)










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



