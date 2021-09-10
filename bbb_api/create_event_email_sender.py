from library.mailchimp import send_mail
from datetime import datetime, timedelta


def event_registration_mail(email, event_name, time, stream_url):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "your event has been registered"
    if stream_url != "":
        text = "your cast {} has been registered at {} UTC. the stream url for the cast is {}".format(event_name, time, stream_url)
    else:
        text = "your event {} has been registered at {}.".format(event_name, time)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status


def event_reminder_mail(email, event_name):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "Reminder email for your event"
    text = "your event {} is going to start in 10 minutes. Please do not miss it.".format(event_name)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status

def attendee_mail(invitee_name, email, event_name, time, meeting_url, attendee_password, stream_url):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "Invitation"
    if stream_url != "":
        text = "Dear {}, <br> You have been invited to join a cast '{}'. <br>The cast will begin at {} UTC. <br>Your cast url is {}. <br>Your stream url is {}. <br>Please provide your name and following password: {}. <br>Don't miss it.".format(invitee_name, event_name, time, meeting_url, stream_url, attendee_password)
    else:
        text = "<p> Dear {}, </p>" \
               "<p>You have been invited to join a cast '{}'. </p>" \
               "<p>The cast will begin at {} UTC. <br>Your cast url is {}. </p>" \
               "<p>Please provide your name and following password: {}. </p>" \
               "<p>Don't miss it!</p>".format(invitee_name, event_name, time, meeting_url, attendee_password)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
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



