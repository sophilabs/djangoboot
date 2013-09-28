from base import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['djangoboot.com']


MEDIA_BUCKET = 'djangoboot-static'
MEDIA_URL = 'http://d2n6mhm0pe75h0.cloudfront.net/'
MEDIA_DOMAIN = 'd2n6mhm0pe75h0.cloudfront.net'
DEFAULT_FILE_STORAGE = 'core.storage.MediaStorage'


STATIC_BUCKET = 'djangoboot-media'
STATIC_URL = 'http://dhcgtpvyqjrjc.cloudfront.net/'
STATIC_DOMAIN = 'dhcgtpvyqjrjc.cloudfront.net'
STATICFILES_STORAGE = 'core.storage.MediaStorage'