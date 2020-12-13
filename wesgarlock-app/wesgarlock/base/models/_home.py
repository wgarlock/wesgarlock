from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel

from ._base import BasePage


class HomePage(BasePage):
    template = "home/home_page.jinja"
    serializer = "wesgarlock.base.serializers:HomePageSerializer"
    primary_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="primary_homepage_link"
    )
    secondary_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="secondary_homepage_link"
    )
    hero_image = models.ForeignKey(
        get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True
    )
    about_image = models.ForeignKey(
        get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True
    )
    about_me = RichTextField()

    content_panels = BasePage.content_panels + [
        PageChooserPanel('primary_page'),
        PageChooserPanel('secondary_page'),
        ImageChooserPanel('hero_image'),
        ImageChooserPanel('about_image'),
        FieldPanel("about_me")
    ]

    api_fields = BasePage.api_fields + [
        'primary_page',
        'secondary_page',
        'hero_image',
        'about_image'
    ]

    class Meta:
        verbose_name = "home_page"
        verbose_name_plural = "home_pages"
