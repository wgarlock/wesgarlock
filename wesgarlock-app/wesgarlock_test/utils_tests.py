from django.conf import settings

from constants import SINGLE_TEST_DATABASE
from fixtures.base import (  # noqa
    create_test_database, create_test_database_no_teardown
)
from fixtures.request import HostNameRequestFactory as rf
from wesgarlock.tenant.exceptions import TenantDatabaseDoesNotExists
from wesgarlock.tenant.utils import (
    connect_database, destroy_database, establish_connection,
    get_database_connection, hostname_from_request, tenant_from_request
)


def test_hostname_from_request():
    request = rf(host_name="test.testserver.com").get("/")
    assert hostname_from_request(request) == "test.testserver.com"


def test_tenant_from_request():
    request = rf(host_name="test.testserver.com").get("/")
    assert tenant_from_request(request) == "test"


def test_tenant_from_request_blacklist():
    request = rf(host_name="test.localhost").get("/")
    assert tenant_from_request(request) == settings.DATABASES["default"]["NAME"]


def test_does_not_exist_establish_connection():
    db = "does_not_exist"
    assert establish_connection(db) is None


def test_get_database_connection(db):
    assert get_database_connection(settings.DATABASES["default"]["NAME"]) is not None


def test_not_get_database_connection():
    assert get_database_connection("does_not_exist") is None


def test_tenant_db_from_request():
    request = rf(host_name="test.testserver.com").get("/")
    assert tenant_from_request(request) == "test"


def test_create_database(create_test_database): # noqa
    assert establish_connection(SINGLE_TEST_DATABASE) is not None


def test_connect_database(create_test_database): # noqa
    try:
        connect_database(SINGLE_TEST_DATABASE)
        assert True
    except TenantDatabaseDoesNotExists:
        assert False


def test_destroy_database(create_test_database_no_teardown):  # noqa
    try:
        destroy_database(SINGLE_TEST_DATABASE)
        assert True
    except TenantDatabaseDoesNotExists:
        assert False
