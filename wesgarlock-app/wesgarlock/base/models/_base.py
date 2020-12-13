from __future__ import unicode_literals

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.urls import include
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel
)
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Collection, Orderable, Page, Site
from wagtail.images import get_image_model_string
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel

from wesgarlock.base.utils import get_class
from wesgarlock.base.validators import hex_validate


class SeriailizerMixin:
    serializer = ""

    @classmethod
    def serializer_model(self):
        return get_class(self.serializer)

    def serialize(self):
        return self.serializer_model()(self).data

    def serialize_all(self):
        return self.serializer_model()(self, many=True).data


class SiteContent(SeriailizerMixin, ClusterableModel):
    site = models.OneToOneField(
        'wagtailcore.Site',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='site_content'
    )
    logo = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='site_logo'
    )
    navigation = models.ManyToManyField(
        'wagtailcore.Page'
    )
    footer_content = models.TextField()

    site_phone = models.CharField(max_length=16)
    site_email = models.EmailField(max_length=255)

    panels = [
        FieldPanel('logo'),
        FieldPanel('site_phone'),
        FieldPanel('site_email'),
        FieldPanel('navigation'),
        InlinePanel('social_media', label='Social Media links'),
        FieldPanel('footer_content')
    ]

    serializer = "wesgarlock.base.serializers:SiteContentSerializer"


class SocialMedia(Orderable):
    site = ParentalKey(
        SiteContent,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='social_media'
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    url = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )
    icon = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )


class SiteColor(ClusterableModel):
    site = ParentalKey(
        SiteContent,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='site_colors'
    )
    js_name = models.CharField(max_length=255)
    is_list = models.BooleanField(default=False)

    panels = [
        FieldPanel('site'),
        FieldPanel('js_name'),
        FieldPanel('is_list'),
        InlinePanel('colors', label='Colors'),
    ]

    def __str__(self):
        if self.js_name:
            return self.js_name
        else:
            return super().__str__()


class Color(models.Model):
    class TYPE(models.TextChoices):
        NONE = "none", _("None")
        MAIN = "main", _("Main")
        LIGHT = "light", _("Light")
        DARK = "dark", _("Dark")
        DARKBLACK = "darkBlack", _("Dark Black")
        BLACK = "black", _("Black")

    site_color = ParentalKey(
        SiteColor,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='colors'
    )
    type = models.CharField(max_length=255, choices=TYPE.choices, default=TYPE.MAIN)
    hex_color = models.CharField(max_length=7, validators=[hex_validate], default="#000000")

    class Meta:
        unique_together = ("type", "site_color")


class BaseMixin(SeriailizerMixin):
    def context_builder(self, request):
        context = dict()
        cache_key = "base_context-{path}-{host}".format(
            path=request.path,
            host=request.get_host()
        )
        context['base_context'] = cache.get(cache_key)
        if not context['base_context']:
            if hasattr(self, 'get_site'):
                site = self.get_site()
            else:
                site = Site.find_for_request(request)
            context['base_context'] = dict()
            SiteContentSerializer = SiteContent.serializer_model()
            context['base_context']['site'] = SiteContentSerializer(
                SiteContent.objects.filter(site=site).first()
            ).data
            context['base_context']['page_api_url'] = reverse('wagtailapi:pages:listing')
            context['base_context']['document_api_url'] = reverse('wagtailapi:documents:listing')
            context['base_context']['image_api_url'] = reverse('wagtailapi:images:listing')
            context['base_context']['scheme'] = request.is_secure() and 'https' or 'http'
            collection = Collection.objects.filter(name="Public").first()
            if collection:
                context['base_context']['site']["public_collection"] = collection.pk
            else:
                context['base_context']['site']["public_collection"] = None
            auth = dict()
            [
                auth.update({url.name: reverse(url.name)})
                for url in include('wesgarlock.front.urls')[0].context_patterns
            ]
            context['base_context']['front_urls'] = auth
            cache.set(cache_key, context['base_context'])
        return context

    def get_context_data(self):
        return self.context_builder(self.request)

    def get_context(self, request):
        self.request = request
        context = super().get_context(request)
        context.update(self.context_builder(self.request))
        return context


class BasePageMixin(BaseMixin):
    serializer = "wesgarlock.base.serializers:BasePageSerializer"
    def context_builder(self, request):
        context = super().context_builder(request)
        context['base_context']['is_authenticated'] = request.user.is_authenticated
        context['base_context']['page'] = self.serialize()
        return context


class BasePage(BasePageMixin, Page):

    description = RichTextField(default='')
    meta_description = models.CharField(max_length=120, blank=True, null=True)
    og_description = models.CharField(max_length=300, blank=True, null=True)
    og_image = models.ForeignKey(
        get_image_model_string(), null=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('meta_description', help_text='in browser text: max chars 120'),
            FieldPanel('og_description', help_text='social media text: max chars 300'),
            ImageChooserPanel('og_image'),
        ], 'Open Graph Content'),
    ]

    api_fields = [
        APIField('description'),
        APIField('og_image_400', serializer=ImageRenditionField('width-400', source='og_image')),
        APIField('og_image_800', serializer=ImageRenditionField('width-800', source='og_image')),
        APIField('og_image_1920', serializer=ImageRenditionField('width-1920', source='og_image'))
    ]

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if len(self.title) > 60:
            raise ValidationError('Must be at least 60 or less chars.')
        if self.og_description == '':
            self.og_description = self.meta_description
        return result

    class Meta:
        abstract = True
        verbose_name = _('basepage')
        verbose_name_plural = _('basepages')
