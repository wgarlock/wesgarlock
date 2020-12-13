import secrets

import pytest
from django.contrib.auth import get_user_model
from wagtail.core.models import Page

from constants import SINGLE_TEST_DATABASE
from wesgarlock.tenant.models import Tenant
from wesgarlock.tenant.utils import create_database, destroy_database

User = get_user_model()

tenanta_domain = "tenanta"
tenantb_domain = "tenantb"

tenant_fixture = [
    dict(
        domain=tenanta_domain,
        name="Tenant A",
    ),
    dict(
        domain=tenantb_domain,
        name="Tenant B",
    )
]

malformed_tenant_fixture = [
    dict(
        domain="tenantA",
        name="Tenant AM",
    ),
    dict(
        domain="tenantB",
        name="Tenant BM",
    )
]


user_fixture = [
    dict(
        email="master@master.com",
        salt=secrets.token_hex(8),
        is_superuser=True,
        is_staff=True,
        password="test123"
    ),
    dict(
        email="tenantownerA@tenantowner.com",
        salt=secrets.token_hex(8),
        is_superuser=False,
        is_staff=False,
        password="test123"
    ),
    dict(
        email="tenantownerB@tenantowner.com",
        salt=secrets.token_hex(8),
        is_superuser=False,
        is_staff=False,
        password="test123"
    ),
    dict(
        email="tenantuserA@tenantuserA.com",
        salt=secrets.token_hex(8),
        is_superuser=False,
        is_staff=False,
        password="test123"
    ),
    dict(
        email="tenantuserB@tenantuserB.com",
        salt=secrets.token_hex(8),
        is_superuser=False,
        is_staff=False,
        password="test123"
    ),
    dict(
        email="masterunassgined@master.com",
        salt=secrets.token_hex(8),
        is_superuser=False,
        is_staff=False,
        password="test123"
    ),
]


@pytest.fixture
def root_page(db) -> Page:
    return Page.objects.create(
        title="DefaultTestPage",
        depth=0,
        path='test'
    )


@pytest.fixture
def users(db) -> User:
    return [User.objects.create_user(**user) for user in user_fixture]


@pytest.fixture
def tenants(db) -> Tenant:
    [Tenant.objects.create(**tenant) for tenant in tenant_fixture]
    yield Tenant.objects.all()
    for tenant in Tenant.objects.all():
        destroy_database(tenant.domain)


@pytest.fixture
def malformed_tenants(db) -> Tenant:
    [Tenant.objects.create(**tenant) for tenant in malformed_tenant_fixture]
    yield Tenant.objects.all()
    for tenant in Tenant.objects.all():
        destroy_database(tenant.domain)


@pytest.fixture
def create_test_database():
    yield create_database(SINGLE_TEST_DATABASE)
    destroy_database(SINGLE_TEST_DATABASE)


@pytest.fixture
def create_test_database_no_teardown():
    yield create_database(SINGLE_TEST_DATABASE)
