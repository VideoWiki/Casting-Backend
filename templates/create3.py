from api.global_variable import CLIENT_DOMAIN_URL

def email_create3(user_name, event_name, event_time, nft_drop_url, meeting_url, moderator_password, attendee_password, pre_reg_url):
    template_part1 = """\
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cancelled</title>
    </head>
    <body>
        Dear {},
    <br>
    <br>
    Your cast <b>{}</b> has been created for <b>{}</b>.
    <br>
    Here is the link for cast: {}
    <br>
    Here is the link for nft drop: {} 
    <br>
    Password for moderator: <b>{}</b> and attendee: <b>{}</b>
    <br>
    Please visit {}/mycasts to initiate the cast.
    <br>
    Here is the link for <b>Pre Registration form: {}<b>
    <br>
    <br>   
     All the best,
    <br>
    VideoWiki team
    </body>
    </html>


    """.format(user_name, event_name, event_time, meeting_url, nft_drop_url, moderator_password, attendee_password, CLIENT_DOMAIN_URL, pre_reg_url)
    return template_part1


def email_create3_otp(user_name, event_name, event_time, nft_drop_url, meeting_url, pre_reg_url):
    template_part1 = """\
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cancelled</title>
    </head>
    <body>
        Dear {},
    <br>
    <br>
    Your cast <b>{}</b> has been created for <b>{}</b>.
    <br>
    Here is the link for cast: {}
    <br>
    Here is the link for nft drop: {} 
    <br>
    Please visit {}/mycasts to initiate the cast.
    <br>
    Here is the link for <b>Pre Registration form: {}<b>
    <br>
    <br>    
    All the best,
    <br>
    VideoWiki team
    </body>
    </html>


    """.format(user_name, event_name, event_time, meeting_url, nft_drop_url, CLIENT_DOMAIN_URL, pre_reg_url)
    return template_part1