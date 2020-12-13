from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BaseConfig(AppConfig):
    name = 'wesgarlock.base'
    label = 'wesgarlockbase'
    verbose_name = _("Wes Garlock Base")

    def ready(self):
        from wesgarlock.base.conf import BaseAppConf  # noqa
