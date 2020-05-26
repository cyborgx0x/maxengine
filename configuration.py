import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'content.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False