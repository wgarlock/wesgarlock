from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wesgarlock.tenant.models import Tenant


class TenantPermissionHelper(PermissionHelper):
    pass


class TenantModelAdmin(ModelAdmin):
    model = Tenant
    permission_helper_class = TenantPermissionHelper
    add_to_settings_menu = True


modeladmin_register(TenantModelAdmin)
