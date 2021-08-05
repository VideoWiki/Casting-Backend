import mandrill
from api.global_variable import MANDRILL_API_KEY


def send_mail( to_email, name,subject, global_merge_vars, text):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'from_email': 'puneet@boarded.in',
            'from_name': 'Puneet Gupta',
            'global_merge_vars': global_merge_vars,
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': subject,
            'tags': ['password-resets'],
            'text': str(text),
            'to': [{'email': to_email,
                    'name': name,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e.text))
