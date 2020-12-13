from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.admin.forms import WagtailAdminModelForm

from wesgarlock.tenant.constants import SITE_OWNER_GROUP_NAME
from wesgarlock.tenant.utils import connect_database, establish_connection


class Tenant(ClusterableModel):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True, db_index=True)
    base_form_class = WagtailAdminModelForm

    panels = [
        FieldPanel('name', classname='fn'),
        FieldPanel('domain', classname='ln'),
        InlinePanel('tenant_owners', label="Owner"),
    ]

    def __str__(self):
        return self.name


class TenantOwnerManager(models.Manager):
    def create_tenantowner(self, _user, database, is_staff, password=None):
        User = get_user_model()
        local_user, created = User.objects.db_manager(using=database).update_or_create(
            email=_user.email,
            defaults=dict(
                is_staff=is_staff
            )
        )

        if local_user and password:
            local_user.set_password(password)
            local_user.save()

        group = Group.objects.db_manager(using=database).get(
            name=SITE_OWNER_GROUP_NAME
        )
        group.user_set.add(local_user)

    def remove_tenantowner(self, instance):
        if not establish_connection(instance.tenant.hostname):
            connect_database(instance.tenant.hostname)

        group = Group.objects.db_manager(using=instance.tenant.hostname).get(
            name=SITE_OWNER_GROUP_NAME
        )
        group.user_set.remove(instance.user)


class TenantOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_owner"
    )
    tenants = ParentalKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="tenant_owners"
    )

    objects = TenantOwnerManager()
