import ConfigParser
import os

HOME_DIR = os.path.expanduser('~')

# Read twitter credentials (username and password)
TWITTER_CRED = os.path.join(HOME_DIR, '.tcred')

conf = ConfigParser.ConfigParser()
with open(TWITTER_CRED, 'rb') as fp:
    conf.readfp(fp)
    USERNAME = conf.get('cred', 'username')
    PASSWORD = conf.get('cred', 'password')


# Read MySQL credentials (password)
DB_CRED = os.path.join(HOME_DIR, '.my.cnf')
with open(DB_CRED, 'rb') as fp:
    conf.readfp(fp)
    DB_PASSWORD = conf.get('client', 'password')

del conf


# MySQL DB conf dictionary
FREQUENCY_STORE = {
    'db':'twitter',
    'table': {
        'name': 'frequency',
        'def':
            '(year int, month int, day int, hour int, minute int, word text)'
        }
    }

FREQUENCY_STORE['connpar'] = {
    'host':'localhost',
    'user':'root',
    'passwd':DB_PASSWORD}


# RabbitMQ set-up
RABBIT_SERVER = 'localhost'
QUEUE_NAME = 'tweet_queue'


# Degree of multi-threading in consumer
PER_CONSUMER_THREADS = 1

