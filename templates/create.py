def email_create(user_name, event_name, event_time, event_url):
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
    Here is the link for stream: {} 
    <br>
    <br>
    All the best,
    <br>
    VideoWiki team
    </body>
    </html>


    """.format(user_name, event_name, event_time, event_url)
    return template_part1