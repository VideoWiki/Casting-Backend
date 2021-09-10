from library.mailchimp import send_mail

def delete_mailer(obj):
    m_list = obj.moderators
    event_name = obj.event_name
    creator_name = obj.event_creator_name
    for i in m_list:
        event_cancelled_mail(m_list["email"],
                             m_list["name"],
                             event_name,
                             creator_name)



def event_cancelled_mail(email, user_name, event_name, creator_name):
    name = email.split('@')[0]
    global_merge_vars = [
        {
            'name': 'NAME',
            'content': name
        }

    ]
    subject = "your event has been cancelled"
    text = "Dear {}" \
           "Your event {} was cancelled by {}. Once the presenter reschedules it, you'll be receiving a new link." \
           "All the best," \
           "VideoWiki team".format(user_name, event_name, creator_name)
    status_res = send_mail(email, name, subject, global_merge_vars, text)
    status = status_res
    return status






