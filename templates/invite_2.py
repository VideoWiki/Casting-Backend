def email_invite2(user_name, event_name, event_time, event_url, event_password, stream_url):
    template_part1 = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marta Getboarded: and for attendee</title>
</head>
<body>

Dear {},
<br>
<br>

You have been invited to join a cast <b>{}</b>, as a co-host. The cast will begin at <b>{}</b>. 
<br>
Your cast url is {}. 
<br>
Please join, provide your name and the following password: <strong>{}</strong>
<br>
Your stream url is {}.
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url, event_password, stream_url)
    return template_part1