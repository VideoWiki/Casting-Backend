from datetime import datetime, timedelta
from cast_invitee_details.helper import send_invite_mail1, \
    send_invite_mail2, send_invite_mail3, \
    send_invite_mail4, send_invite_mail5, send_invite_mail_cohost,\
    send_invite_mail_part_vm, send_invite_mail_viewer, \
    send_invite_mail_spec, send_invite_mail_otp, send_invite_mail_pass

from bbb_api.create_event_api.helper import send_create1, send_create2, send_create3,\
    send_create4, send_create6, send_create5, send_create7, send_create8,\
    send_create9, send_create10
import pytz


def event_registration_mail(email, user_name, event_name, time, stream_url, meeting_url,
                            nft_drop_url, moderator_password, attendee_password, send_otp,
                            pre_reg_url, start_time, event_type, viewer_mode, viewer_password):
    if event_type == "public":
        if stream_url == "" and viewer_mode == False:
            print("here")
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
                  creator_email, viewer_mode, public_otp, viewer_pass):
    if cast_type == "public":
        if role == "participant" and viewer_mode == False:
            send_invite_mail4(to_email=email, user_name=user_name, event_name=event_name,
                              event_time= event_time, event_url=event_url, dt=dt,
                              creator_nmae=creator_nmae, creator_email=creator_email,
                              role=role)
        elif role == "co-host":
            send_invite_mail_cohost( user_name=user_name, to_email=email,
                                     event_name=event_name, event_time=event_time,
                                     event_url=event_url, dt=dt, creator_nmae=creator_nmae,
                                     creator_email=creator_email, role=role, password=co_password)
        elif role == "participant" and viewer_mode == True:
            send_invite_mail_part_vm(user_name, email, event_name, event_time, event_url, dt, creator_nmae,
                                     creator_email, role, event_password)
        elif role == "viewer" and viewer_mode == True:
            send_invite_mail_viewer(user_name, email, event_name, event_time, event_url, dt, creator_nmae,
                                    creator_email, role)
        elif role == "spectator" and stream_url != "":
            print(stream_url, 'su')
            send_invite_mail_spec(user_name, email, event_name, event_time, stream_url, dt, creator_nmae,
                                  creator_email, role)

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



