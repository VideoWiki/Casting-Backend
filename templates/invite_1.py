def email_invite1_mod(user_name, event_name, event_time, event_url, event_password):
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
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url, event_password)
    return template_part1


def email_invite_participant(user_name, event_name, event_time, event_url, event_password):
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

You have been invited to join a cast as <b>{}</b>, as a participant. The cast will begin at <b>{}</b>. 
<br>
Your cast url is {}. 
<br>
Please join, provide your name and the following password: <strong>{}</strong>
<br>
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url, event_password)
    return template_part1

def email_invite_viewer(user_name, event_name, event_time, event_url, event_password):
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

You have been invited to join a cast as <b>{}</b>, as a viewer. The cast will begin at <b>{}</b>. 
<br>
Your cast url is {}. 
<br>
Please join, provide your name and the following password: <strong>{}</strong>
<br>
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url, event_password)
    return template_part1


def email_invite_spectator(user_name, event_name, event_time, stream_url):
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

You have been invited to join the stream <b>{}</b>,on VideoWiki Cast. It will begin at <b>{}</b>. 
<br>
Your stream url is {}
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, stream_url)
    return template_part1


def email_invite1_mod_otp(user_name, event_name, event_time, event_url):
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
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url)
    return template_part1


def email_invite_participant_otp(user_name, event_name, event_time, event_url):
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

You have been invited to join a cast as <b>{}</b>, as a participant. The cast will begin at <b>{}</b>. 
<br>
Your cast url is {}. 
<br>
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url)
    return template_part1


def email_invite_viewer_otp(user_name, event_name, event_time, event_url):
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

You have been invited to join a cast as <b>{}</b>, as a viewer. The cast will begin at <b>{}</b>. 
<br>
Your cast url is {}. 
<br>
<br>

Don't miss it! We're looking forward to see you there.
</body>
</html>


    """.format(user_name, event_name, event_time, event_url)
    return template_part1