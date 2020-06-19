# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from rest_framework import serializers
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.fields import RichTextField
from wagtail.search import index

from wesgarlock.base.models import BasePage
from wesgarlock.base.serializers import BasePageSerializer


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')
    parent_page_types = ['wesgarlockblog.BlogTagIndexPage']


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPageTag
        fields = "__all__"


class BlogPageSerializer(BasePageSerializer):

    date = serializers.DateField()
    intro = serializers.CharField()
    body = serializers.CharField()
    tags = BlogTagSerializer(many="True", read_only=True)

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + [
            "date", "intro", "body", "tags"
        ]


class BlogPage(BasePage):
    template = "blog/blog_page.jinja"
    parent_page_types = ['wesgarlockblog.BlogIndexPage']
    date = models.DateField("Post date")
    intro = models.CharField(max_length=1000, blank=True, null=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField('tags'),
    ]

    content_panels = BasePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('intro'),
        ], heading="Blog information"),
        FieldPanel('body', classname='full'),
    ]

    api_fields = BasePage.api_fields + [
        APIField("date"),
        APIField("tags"),
        APIField("intro"),
        APIField("body")
    ]

    serializer = "wesgarlock.blog.serializers:BlogPageSerializer"

    class Meta:
        verbose_name = _('Blog Page')
        verbose_name_plural = _('Blog Pages')


class BlogIndexPage(RoutablePageMixin, BasePage):
    parent_page_types = ['wesgarlockbase.HomePage']
    template = "blog/blog_index_page.jinja"

    class Meta:
        verbose_name = _('Blog Index Page')
        verbose_name_plural = _('Blog Index Pages')
