import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


# basedir = os.path.abspath(os.path.dirname(__file__))
# + os.path.join(basedir, 'app.db'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hey rakesh"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', True)

    # Configuration for Sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'mysql+mysqlconnector://rakeshmicroblog:mysql123@rakeshmicroblog.mysql.pythonanywhere-services.com:3306/rakeshmicroblog$microblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration for Email..
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'rakeshkumar.18172@marwadieducation.edu.in'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ndandqptnrjiyvyj'
    ADMINS = ['rakesh0506907@gmail.com']

    # Configuration for pagination..
    POSTS_PER_PAGE = 3  # recommended 25
    FOLLOWERS_PER_PAGE = 10
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    # Credentials of Social Authentication Providers

    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')


class CeleryConfig:
    CELERY_IMPORTS = ('app.main.tasks',)
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERYBEAT_SCHEDULE = {
        'every-minute_add': {
            'task': 'app.main.tasks.every_minute_add',
            'schedule': timedelta(seconds=2),
            'args': (3, 4)
        },
        'every-minute_multiply': {
            'task': 'app.main.tasks.every_minute_multiply',
            'schedule': timedelta(seconds=2),
            'args': (3, 4)
        },
    }
