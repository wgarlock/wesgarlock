from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from wagtail.core.models import Page, Site
from wagtail.images.models import Image

from wesgarlock.base.models import HomePage, Message, SocialMedia
from wesgarlock.base.validators import hex_validate


class ImageRenditionField(Field):
    def __init__(self, **kwargs):
        self.filter = kwargs["kwargs"].get('filter', None)
        super().__init__(kwargs)

    def get_attribute(self, instance):
        return instance

    def to_representation(self, image, **kwargs):
        if self.filter:
            return image.get_rendition(filter=self.filter).file.url
        else:
            return image.file.url


class ImageModelSerializer(serializers.ModelSerializer):
    jpeg_400 = ImageRenditionField(read_only=True, kwargs={"filter": "width-400|format-jpeg"})
    jpeg_800 = ImageRenditionField(read_only=True, kwargs={"filter": "width-800|format-jpeg"})
    jpeg_1920 = ImageRenditionField(read_only=True, kwargs={"filter": "width-1920|format-jpeg"})

    class Meta:
        model = Image
        fields = ("id", "title", "collection", "jpeg_400", "jpeg_800", "jpeg_1920")


class PageUrlField(serializers.Field):
    def to_representation(self, value):
        return value


class NavigationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    url = PageUrlField()


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "title", "slug", "live", "seo_title", "content_type", "url"]


class BasePageSerializer(PageSerializer):
    description = serializers.CharField()

    class Meta(PageSerializer.Meta):
        fields = PageSerializer.Meta.fields + [
            "description"
        ]


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


class ColorListSerializer(serializers.ListSerializer):

    def create_rep(self, item, obj):
        if not item.site_color.is_list:
            obj.update({item.type: item.hex_color})
            return obj
        else:
            if not isinstance(obj, list):
                obj = [item.hex_color]
            else:
                obj.append(item.hex_color)

            return obj

    def to_representation(self, data):
        obj = dict()
        iterable = data.all() if isinstance(data, models.Manager) else data
        for item in iterable:
            obj = self.create_rep(item, obj)
        return obj

    @property
    def data(self):
        super().data
        return ReturnDict(self._data, serializer=self)

    @property
    def data_list(self):
        super().data
        return ReturnList(self._data, serializer=self)


class ColorSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=255)
    hex_color = serializers.CharField(validators=[hex_validate])

    class Meta:
        list_serializer_class = ColorListSerializer


class SiteColorListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        obj = dict()
        iterable = data.all() if isinstance(data, models.Manager) else data
        [
            obj.update({item.js_name: ColorSerializer(item.colors, many=True).data})
            if not item.is_list else obj.update({item.js_name: ColorSerializer(item.colors, many=True).data_list})
            for item in iterable
        ]
        return obj


class SiteColorSerializer(serializers.Serializer):
    js_name = serializers.CharField(max_length=255)
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = SiteColorListSerializer


class SiteContentSerializer(serializers.Serializer):
    site = SiteSerializer(many=False, read_only=True)
    logo = ImageModelSerializer(many=False, read_only=True)
    navigation = PageSerializer(many=True, read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    site_colors = SiteColorSerializer(many=True, read_only=True)
    footer_content = serializers.CharField(read_only=True)
    site_phone = serializers.CharField(read_only=True)
    site_email = serializers.EmailField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ["thread"]


class HomePageSerializer(BasePageSerializer):
    hero_image = ImageModelSerializer()
    about_image = ImageModelSerializer()

    class Meta(BasePageSerializer.Meta):
        model = HomePage
        fields = BasePageSerializer.Meta.fields + [
            "primary_page", "secondary_page", "about_me",
            "about_image", "hero_image"
        ]
