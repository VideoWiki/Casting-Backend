def email_invite1(user_name, event_name, event_time, event_url, event_password):
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

You have been invited to join a cast <b>{}</b>. The cast will begin at <b>{}</b>. 
<br>
Your cast url is {}. 
<br>
Please join, provide your name and the following password: <strong>{}</strong>
<br>
<br>

Don't miss it!
</body>
</html>


    """.format(user_name, event_name, event_time, event_url, event_password)
    return template_part1