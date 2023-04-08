import mandrill
from api.global_variable import MANDRILL_API_KEY
from templates.nftmailer import nft_mailer

mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)

def nft_drop_mail(to_email, subject, nft_url):
    message = {
        'from_email': 'support@videowiki.pt',
        'from_name': 'VideoWiki',
        'to': [{'email': to_email, 'type': 'to'}],
        'subject': subject,
        'merge_language': 'mailchimp',
        'merge_vars': [
            {
                'rcpt': to_email,
                'vars': [

                    {
                        'name': 'nft_link',
                        'content': nft_url
                    }
                ]
            }
        ],
        'tags': ['VW-NFT-DROP'],
        'template_name': 'VW-NFT-DROP'
    }

    # Send the message
    result = mandrill_client.messages.send_template(template_name=message['template_name'], template_content=[], message=message)

    # Print the result
    print(result)
    return result