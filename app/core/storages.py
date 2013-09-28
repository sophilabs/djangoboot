from storages.backends.s3boto import S3BotoStorage
from django.contrib.staticfiles.storage import CachedFilesMixin
from django.conf import settings


class MediaStorage(S3BotoStorage):
    """ Media files storage.
    """

    def __init__(self, *args, **kwargs):
        super(MediaStorage, self).__init__(
            bucket=settings.MEDIA_BUCKET,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            headers=settings.MEDIA_HEADERS,
            location=settings.MEDIA_LOCATION,
            custom_domain=settings.MEDIA_DOMAIN,
            gzip=True)


class StaticStorage(CachedFilesMixin, S3BotoStorage):
    """ Static files storage.
    """

    def __init__(self, *args, **kwargs):
        super(StaticStorage, self).__init__(
            bucket=settings.STATIC_BUCKET,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            headers=settings.STATIC_HEADERS,
            location=settings.STATIC_LOCATION,
            custom_domain=settings.STATIC_DOMAIN,
            gzip=True)