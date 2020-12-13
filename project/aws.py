from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'private'
    file_overwrites = False


class MediaRootStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'
    file_overwrites = False
