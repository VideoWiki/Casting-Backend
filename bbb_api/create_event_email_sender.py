from library.mailchimp import send_mail
from datetime import datetime, timedelta
from cast_invitee_details.helper import send_invite_mail1, \
    send_invite_mail2, send_invite_mail3, \
    send_invite_mail4, send_invite_mail5
from bbb_api.create_event_api.helper import send_create1, send_create2, send_create3, send_create4
import pytz


def event_registration_mail(email, user_name, event_name, time, stream_url, meeting_url, nft_drop_url, moderator_password, attendee_password):
    if stream_url != "" and nft_drop_url == "":
        send_create1(email, user_name, event_name, time, stream_url, meeting_url, moderator_password, attendee_password)
    elif stream_url == "" and nft_drop_url != "":
        send_create3(email, user_name, event_name, time, nft_drop_url, meeting_url, moderator_password, attendee_password)
    elif stream_url != "" and nft_drop_url != "":
        send_create4(email, user_name, event_name, time, stream_url, nft_drop_url, meeting_url, moderator_password, attendee_password)
    else:
        send_create2(email, user_name, event_name, time, meeting_url, moderator_password, attendee_password)


def attendee_mail(user_name, email, event_name, event_time, event_url, event_password, stream_url, role):
    if role == "co-host":
        if stream_url != "":
            send_invite_mail2(to_email=email,
                              user_name= user_name,
                              event_name= event_name,
                              event_time= event_time,
                              event_url= event_url,
                              stream_url= stream_url,
                              event_password= event_password
                              )
        else:
            send_invite_mail1(to_email= email,
                              user_name= user_name,
                              event_name= event_name,
                              event_time= event_time,
                              event_url= event_url,
                              event_password= event_password
                              )
    elif role == "spectator":
        send_invite_mail3(to_email= email,
                          user_name= user_name,
                          event_name= event_name,
                          event_time= event_time,
                          stream_url= stream_url
                          )
    elif role == "participant":
        send_invite_mail4(to_email= email,
                          user_name= user_name,
                          event_name= event_name,
                          event_time= event_time,
                          event_url= event_url,
                          event_password= event_password
                          )
    elif role == "viewer":
        send_invite_mail5(to_email= email,
                          user_name= user_name,
                          event_name= event_name,
                          event_time= event_time,
                          event_url= event_url,
                          event_password= event_password
                          )





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



