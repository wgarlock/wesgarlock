from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wesgarlock.base.models import MessageThread, SiteColor, SiteContent


class SiteContentAdmin(ModelAdmin):
    model = SiteContent
    menu_label = 'Site Content'
    menu_icon = 'doc-empty'
    menu_order = 200
    add_to_settings_menu = True
    exclude_from_explorer = False


class SiteColorAdmin(ModelAdmin):
    model = SiteColor
    menu_label = 'Site Palette'
    menu_icon = 'doc-empty'
    menu_order = 200
    add_to_settings_menu = True
    exclude_from_explorer = False


class MessageThreadAdmin(ModelAdmin):
    model = MessageThread
    menu_label = 'Messages'
    menu_icon = 'doc-empty'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False


modeladmin_register(MessageThreadAdmin)
modeladmin_register(SiteContentAdmin)
modeladmin_register(SiteColorAdmin)
