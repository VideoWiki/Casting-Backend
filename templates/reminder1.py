def reminder1(user_name, event_name, event_time, event_url, event_password):
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

Don't forget you have been invited for the event {} for {}. It starts in <strong>10 minutes</strong>.
<br>
Here is the link to join: {}
<br>
Please provide your name and the following password when entering: <strong>{}</strong>
<br><br>

All the best,<br>
VideoWiki team
</body>
</html>

    """.format(user_name, event_name, event_time, event_url, event_password)
    return template_1