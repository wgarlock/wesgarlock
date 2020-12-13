from appconf import AppConf


class BaseAppConf(AppConf):
    DEFAULT_LOGO = "images/wes_logo.png"
    DEFAULT_HERO_IMAGE = "images/snow.jpg"
    DEFAULT_ABOUT_IMAGE = "images/snow.jpg"
    DEFAULT_OG_IMAGE = "images/dog.jpg"

    class Meta:
        prefix = 'base'
