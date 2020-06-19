import psycopg2
from django.conf import settings
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from wesgarlock.tenant.exceptions import (
    TenantDatabaseDoesNotExists, TenantDatabaseExists
)


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    if hostname not in settings.DB_ROUTER_BLACK_LIST_HOSTNAMES:
        subdomain_prefix = hostname.split('.')[0]
        return subdomain_prefix
    return settings.DATABASES["default"]["NAME"]


def tenant_db_from_request(request):
    db = tenant_from_request(request)
    if get_database_connection(db):
        return db
    elif get_database_connection(settings.DATABASES['default']['NAME']):
        return settings.DATABASES['default']['NAME']


def get_database_connection(db):
    if establish_connection(db):
        if connections.databases.get(db, None):
            return db
        connection = connect_database(db)
        if connection:
            return db
        return None


def establish_connection(db):
    try:
        con = psycopg2.connect(
            dbname=db,
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"]
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except psycopg2.OperationalError:
        return None

    return con


def close_connection(db):
    try:
        psycopg2.close(
            dbname=db,
            user=settings.DATABASE_USER,
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"]
        )
    except psycopg2.OperationalError:
        return False

    return True


def create_database(db):
    if not establish_connection(db):
        con = establish_connection(settings.DATABASES["default"]["NAME"])
        with con.cursor() as cursor:
            sqlCreateDatabase = 'create database {db}'.format(
                db=db
            )
            cursor.execute(sqlCreateDatabase)
        return db
    else:
        raise TenantDatabaseExists("Tenant Database {db} currently exists".format(db=db))


def connect_database(db):
    connections.databases[db] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db,
        "USER": settings.DATABASES['default']["USER"],
        "PASSWORD": settings.DATABASES['default']["PASSWORD"],
        "HOST": settings.DATABASES['default']["HOST"],
        "PORT": settings.DATABASES['default']["PORT"]
    }
    return connections[db]


def destroy_database(db):
    database = establish_connection(db)
    if database:
        database.close()
        con = psycopg2.connect(
            dbname=settings.DATABASES['default']["NAME"],
            user=settings.DATABASES['default']["USER"],
            password=settings.DATABASES['default']["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"]
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with con.cursor() as cursor:
            sqlDisconnect = (
                "SELECT pg_terminate_backend(pid)"
                " FROM pg_stat_activity WHERE datname = '{db}';"
            ).format(db=db)
            cursor.execute(sqlDisconnect)
            sqlDeleteDatabase = 'drop database {db}'.format(
                db=db
            )
            cursor.execute(sqlDeleteDatabase)
    else:
        pass
        raise TenantDatabaseDoesNotExists("Tenant Database {db} does not exist".format(db=db))
