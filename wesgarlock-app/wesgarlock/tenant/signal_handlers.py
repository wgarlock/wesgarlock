import os
import secrets

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import (
    post_migrate, post_save, pre_delete, pre_save
)

from wesgarlock.tenant.utils import (
    connect_database, create_database, destroy_database
)


def clean_tenant(sender, instance, **kwargs):
    if instance.domain != instance.domain.lower():
        raise ValidationError("Must be lower case for DB consistancy")


def create_database_on_tenant(sender, instance, created, **kwargs):
    if created:
        db = create_database(instance.domain)
        if db:
            connection = connect_database(db)
            if connection:
                import subprocess
                command = 'python tenant_context_manage.py {db} migrate --database={db}'.format(db=db)
                subprocess.call(command, shell=True, cwd=os.getcwd())
                command = 'python tenant_context_manage.py {db} init_project'.format(db=db)
                subprocess.call(command, shell=True, cwd=os.getcwd())


def pre_created_tenantowner(sender, instance, using, update_fields=[], **kwargs):
    if update_fields and "user" in update_fields and instance.pk:
        from wesgarlock.tenant.models import TenantOwner
        old_instance = TenantOwner.objects.get(id=instance.id)
        TenantOwner.objects.remove_tenantowner(
            instance=old_instance,
        )


def created_tenantowner(sender, instance, created, using, update_fields, **kwargs):
    db = instance.tenants.domain
    connection = connect_database(db)
    if connection:
        from wesgarlock.tenant.models import TenantOwner
        if created:
            if settings.DEBUG:
                password = "test123"
            else:
                password = secrets.token_urlsafe(64)
            TenantOwner.objects.create_tenantowner(
                _user=instance.user,
                password=password,
                database=db,
                is_staff=True
            )
        else:

            TenantOwner.objects.create_tenantowner(
                _user=instance.user,
                database=db,
                is_staff=True
            )


def destroy_database_on_tenant(sender, instance, **kwargs):
    destroy_database(instance.domain)


def migrate_all(sender, **kwargs):
    from wesgarlock.tenant.models import Tenant
    for tenant in Tenant.objects.all():
        import subprocess
        command = 'python tenant_context_manage.py {db} migrate --database={db}'.format(db=tenant.domain)
        subprocess.call(command, shell=True, cwd=os.getcwd())
        command = 'python tenant_context_manage.py {db} init_project'.format(db=tenant.domain)
        subprocess.call(command, shell=True, cwd=os.getcwd())


def register_signal_handlers(app):
    from wesgarlock.tenant.models import Tenant, TenantOwner
    pre_save.connect(clean_tenant, sender=Tenant)
    post_save.connect(create_database_on_tenant, sender=Tenant)
    pre_save.connect(pre_created_tenantowner, sender=TenantOwner)
    post_save.connect(created_tenantowner, sender=TenantOwner)
    pre_delete.connect(destroy_database_on_tenant, sender=Tenant)
    post_migrate.connect(migrate_all, sender=app, dispatch_uid="")
