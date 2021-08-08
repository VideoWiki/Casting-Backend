from library.mailchimp import send_mail
from datetime import datetime


def event_registration_mail(email, event_name, time):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "your event has been registered"
    text = "your event {} has been registered at {} UTC.".format(event_name, time)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status


def event_reminder_mail(email, event_name, time):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "Reminder email for your event"
    text = "your event {} will start at {} UTC. Please do not miss it.".format(event_name, time)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status

def attendee_mail(email, event_name, time, meeting_url, attendee_password):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "Reminder email for your event"
    text = "Your event -'{}' will start at {} UTC. Your event url is {} and event password is -'{}'. " \
           "Please do not miss it.".format(event_name, time, meeting_url, attendee_password)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status

def time_subtractor(time):
    s1 = '00:10:00'
    s2 = '{}:{}:00'.format(time[11:13], time[14:])
    format = '%H:%M:%S'
    subtracted_time = datetime.strptime(s2, format) - datetime.strptime(s1, format)
    print(subtracted_time)
    return subtracted_time

