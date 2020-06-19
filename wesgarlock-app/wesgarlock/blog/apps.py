from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BlogConfig(AppConfig):
    name = 'wesgarlock.blog'
    label = 'wesgarlockblog'
    verbose_name = _("Wes Garlock Blog")
