from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FrontConfig(AppConfig):
    name = 'wesgarlock.front'
    label = 'wesgarlockfront'
    verbose_name = _("Wes Garlock Front")
