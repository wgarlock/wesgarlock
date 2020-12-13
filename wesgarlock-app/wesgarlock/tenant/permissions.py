from wagtail.core.permission_policies import ModelPermissionPolicy

from wesgarlock.tenant.models import Tenant

tenant_permission_policy = ModelPermissionPolicy(Tenant)
