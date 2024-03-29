def reminder_mod1(user_name, role, event_name, event_time, event_url, event_password):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>
    

Dear {},
<br>
<br>

Don't forget you have been invited, as a {}, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
Please provide your name and the following password when entering: <strong>{}</strong>
<br><br>

See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, role, event_name, event_time, event_url, event_password)
    return template_1


def reminder_participant(user_name, role, event_name, event_time, event_url, event_password):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a {}, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
Please provide your name and the following password when entering: <strong>{}</strong>
<br><br>

See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, role, event_name, event_time, event_url, event_password)
    return template_1

def reminder_parti_wo_pass(user_name, role, event_name, event_time, event_url):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a {}, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, role, event_name, event_time, event_url)
    return template_1

def reminder_viewer(user_name, event_name, event_time, event_url, event_password):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a viewer, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
Please provide your name and the following password when entering: <strong>{}</strong>
<br><br>

See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, event_name, event_time, event_url, event_password)
    return template_1


def reminder_spectator(user_name, event_name, event_time, event_url):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a spectator, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Your stream url is {}
<br><br>

See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, event_name, event_time, event_url)
    return template_1


def reminder_mod1_otp(user_name, event_name, event_time, event_url):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a co-host, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>

See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, event_name, event_time, event_url)
    return template_1


def reminder_participant_otp(user_name, event_name, event_time, event_url):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a participant, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>

See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, event_name, event_time, event_url)
    return template_1



def reminder_viewer_otp(user_name, event_name, event_time, event_url):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a viewer, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, event_name, event_time, event_url)
    return template_1

def reminder_pri_unique(user_name, role, event_name, event_time, event_url):
    template_1 = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder for attendee</title>
</head>
<body>


Dear {},
<br>
<br>

Don't forget you have been invited, as a {}, for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
See you soon!,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, role, event_name, event_time, event_url)
    return template_1