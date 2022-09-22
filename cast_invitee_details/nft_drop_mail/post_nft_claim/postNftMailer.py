import mandrill
from api.global_variable import MANDRILL_API_KEY
from templates.postvcmailer import post_vc_mailer

def postCertiMailer( to_email, nft_url, trans_id):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': post_vc_mailer(email=to_email, nft_url= nft_url, trans_id= trans_id),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "GALA NFT Details",
            'tags': ['password-resets'],
            'text': 'Example text content',
            'to': [{'email': to_email,
                    'name': to_email,
                    'type': 'to'}],
        }
        result = mandrill_client.messages.send(message = message)
        print(result)
        status = result[0]["status"]
        return status
    except mandrill.Error as e:
        print("An exception occurred: {}".format(e))