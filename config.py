import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ELASTICSEARCH_URL= 'https://nol0b9gns3:pfh02ezorl@state-8851386751.us-west-2.bonsaisearch.net'
    MYSQL_HOST = 'us-cdbr-iron-east-01.cleardb.net'
    MYSQL_USER = 'b52f569efaaf0b'
    MYSQL_PASSWORD = '8e4e9d41'
    MYSQL_DB = 'heroku_9c26c6619d3062f'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://b52f569efaaf0b:8e4e9d41@us-cdbr-iron-east-01.cleardb.net/heroku_9c26c6619d3062f'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
