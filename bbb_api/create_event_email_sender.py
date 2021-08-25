from library.mailchimp import send_mail
from datetime import datetime


def event_registration_mail(email, event_name, time):
    print(email,"98989")
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

def attendee_mail(invitee_name, email, event_name, time, meeting_url, attendee_password):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "Invitation"
    text = "Dear {}, You have been invited to join a cast -'{}'. The cast will begin at {} UTC. Your cast url is {} and password is -'{}'. " \
           "Please do not miss it.".format(invitee_name, event_name, time, meeting_url, attendee_password)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status

def time_subtractor(time):
    s1 = '00:10:00'
    s2 = '{}:{}:00'.format(time[11:13], time[14:16])
    format = '%H:%M:%S'
    subtracted_time = datetime.strptime(s2, format) - datetime.strptime(s1, format)
    print(subtracted_time)
    return subtracted_time

def time_subtractor2(time):
    s1 = '00:00:30'
    s2 = '{}:{}:00'.format(time[11:13], time[14:16])
    format = '%H:%M:%S'
    subtracted_time = datetime.strptime(s2, format) - datetime.strptime(s1, format)
    print(subtracted_time)
    return subtracted_time

