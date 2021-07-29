import os
development = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

    DATABASE = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }

    ROLLBAR_ACCESS  = {
        'access_token': '0dc5164901214f248c1aa3a338562d44',
        'environment': 'development' if development else 'production',
        'root': BASE_DIR,
    }

