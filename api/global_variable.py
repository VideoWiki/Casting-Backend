import os
from dotenv import load_dotenv
load_dotenv()
development = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_URL = "http://api.cast.video.wiki"
if development == False:
    Q_C = {'orm': 'default', 'sync': True}
    BASE_URL = os.getenv("BASE_URL")

    DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

    ROLLBAR_ACCESS = {
        'access_token': os.getenv("access_token")
    }

    MANDRILL_API_KEY = os.getenv("MANDRILL_API_KEY")
    PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

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
                'access_token': os.getenv("access_token2"),
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
        'access_token': os.getenv("access_token2"),
        'environment': 'development' if development else 'production',
        'root': BASE_DIR,
    }

    MANDRILL_API_KEY = os.getenv("MANDRILL_API_KEY2")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'video.wiki'
AWS_LOCATION = 'us-east-2'
AWS_BASE_URL = 'https://s3.us-east-2.amazonaws.com/video.wiki/media/cover_images/'
BASE_URL_AWS = "http://s3.us-east-2.amazonaws.com/video.wiki/media/"
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#stream_url
STREAM_URL = "https://api.stream.video.wiki/api/cast/live/"
TYPEFORM_URL = "https://api.typeform.com/forms/xQ5sUFNz/responses"
TYPEFORM_URL_PRE_REG = "https://gtbrdd.typeform.com/to/xQ5sUFNz#event_name="
# BBB_API_URL = "https://class.video.wiki/bigbluebutton/"
# SALT = "Mxa621WXrztimJ9swYh38ZORHPyVBN0prSjlN6ftWI"
BBB_API_URL = "https://room.video.wiki/bigbluebutton/"
SALT = os.getenv("SALT")
VERIFY_API_KEY_URL = "https://api.video.wiki/api/verify/key/"