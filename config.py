import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ELASTICSEARCH_URL= ''
    MYSQL_HOST = ''
    MYSQL_USER = ''
    MYSQL_PASSWORD = ''
    MYSQL_DB = ''
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
