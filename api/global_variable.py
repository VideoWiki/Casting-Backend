import os
development = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_URL = "http://api.cast.video.wiki"
if development == False:
    Q_C = {'orm': 'default', 'sync': True}
    BASE_URL = 'http://localhost:8000/'

    DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

    ROLLBAR_ACCESS = {
        'access_token': '3a684ebfdcc34ff69446d583519d5666'
    }

    MANDRILL_API_KEY = "feczsxGoFPR7Kc1Wqdd841Vw"
    PIXABAY_API_KEY = '14852807-36c181b80405fd874ccda74a5f7'

else:
    Q_C = {
        'name': 'casting-backend',
        'workers': 2,
        'recycle': 500,
        'timeout': 1000000,
        'compress': True,
        'save_limit': 20,
        'queue_limit': 500,
        'cpu_affinity': 500,
        "sync": False,
        'label': 'Django Q',
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0, },
        'error_reporter': {
            'rollbar': {
                'access_token': '0dc5164901214f248c1aa3a338562d44',
                'environment': 'Django-Q'
            }
        }
    }
    BASE_URL = "https://api.cast.video.wiki"
    CLIENT_DOMAIN_URL = "https://cast.video.wiki"
    VW_RTMP_URL = "rtmp://play.stream.video.wiki/stream/"


    DATABASE = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }

    ROLLBAR_ACCESS  = {
        'access_token': '0dc5164901214f248c1aa3a338562d44',
        'environment': 'development' if development else 'production',
        'root': BASE_DIR,
    }

    MANDRILL_API_KEY = "feczsxGoFPR7Kc1Wq841Vw"

AWS_ACCESS_KEY_ID = 'AKIAVYPW7ED4TK47VUNP'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'video.wiki'
AWS_LOCATION = 'us-east-2'
AWS_BASE_URL = 'https://s3.us-east-2.amazonaws.com/video.wiki/media/cover_images/'
BASE_URL_AWS = "http://s3.us-east-2.amazonaws.com/video.wiki/media/"
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#stream_url
STREAM_URL = "https://api.stream.video.wiki/api/cast/live/"
TYPEFORM_URL = "https://api.typeform.com/forms/xQ5sUFNz/responses"

# BBB_API_URL = 'https://dev.stream.video.wiki/bigbluebutton/'
BBB_API_URL = 'https://live.event.video.wiki/bigbluebutton/'

# SALT = 'vOIxIbVyXS6xI4qiX94QO1kxoT42ITp58bJb3W1yDKI'
SALT = 'PRatQHfVdKC5qqadJGgUDv3b0Fz9rWOTW4PkfSjF9t4'