def post_vc_mailer(email, nft_url, trans_id):
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
    Congratulations for successfully claiming your <b>Certificate of Recognition by GALA Academy</b>.
    <br>
    Here is the url for your claimed Certificate: {}
    <br>
    Here is the transaction Id: {}
    <br>
    <br>
    All the best,
    <br>
    VideoWiki team
    </body>
    </html>


    """.format(email, nft_url, trans_id)
    return template_part1