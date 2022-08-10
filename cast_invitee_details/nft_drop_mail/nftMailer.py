import mandrill
from api.global_variable import MANDRILL_API_KEY
from templates.nftmailer import nft_mailer

def nftMailer( to_email, nft_drop_url):
    try:
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
        message = {
            'html': nft_mailer(user_name=to_email,
                               nft_drop_url=nft_drop_url),
            'from_email': 'support@videowiki.pt',
            'from_name': 'Video.Wiki',
            'global_merge_vars': [],
            # need reply mail
            'headers': {'Reply-To': 'support@videowiki.pt'},
            'merge': True,
            'merge_language': 'mailchimp',
            'subject': "Claim VideoWiki NFT",
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