import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    '''
     this config file return an dictionary of config
    '''
    SQLALCHEMY_DATABASE_URI =  'mysql+mysqlconnector://root:@localhost:3306/fetch'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
