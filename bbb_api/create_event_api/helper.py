from ..create_event_email_sender import event_reminder_mail

def email_sender(e_list, name, time):

    for email in e_list:
        event_reminder_mail(email, name, time)
    return "sent"