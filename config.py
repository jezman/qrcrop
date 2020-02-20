import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MAX_CONTENT_LENGTH = 160 * 1024 * 1024
    UPLOAD_PATH = os.path.join(basedir, 'originals')
    SPLITTED_PATH = os.path.join(basedir, 'splitted')
    COMPRESSED_PATH = os.path.join(basedir, 'compressed')
    ALLOWED_EXTENSIONS = set(['pdf'])
