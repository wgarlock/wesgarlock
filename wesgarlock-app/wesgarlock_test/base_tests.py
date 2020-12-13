from wagtail.core.models import Group

from fixtures.base import tenants  # noqa
from wesgarlock.tenant.constants import SITE_OWNER_GROUP_NAME
from wesgarlock.tenant.models import Tenant
from wesgarlock.tenant.utils import establish_connection


def test_tenants(db) -> None:
    for tenant in Tenant.objects.all():
        assert establish_connection(tenant.domain) is not None
        assert Group.objects.db_manager(
            using=tenant.domain.lower()
        ).filter(name=SITE_OWNER_GROUP_NAME).first() is not None
