import datetime


class BaseConfig(object):
    UPLOAD_FOLDER = "download"
    MAX_CONTENT_LENGTH = 1024 * 1024
    DURATION = datetime.timedelta(hours=5)
    
