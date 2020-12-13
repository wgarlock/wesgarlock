from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import BaseAPIViewSet, PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images import get_image_model

from wesgarlock.base.serializers import ImageModelSerializer

api_router = WagtailAPIRouter('wagtailapi')


class ImagesAPIViewSet(BaseAPIViewSet):
    base_serializer_class = ImageModelSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    body_fields = ['title', "collection"]
    meta_fields = ["id", "collection", 'jpeg_400', 'jpeg_800', 'jpeg_1920']
    listing_default_fields = BaseAPIViewSet.listing_default_fields + [
        'title', "collection", 'jpeg_400', 'jpeg_800', 'jpeg_1920'
    ]
    nested_default_fields = BaseAPIViewSet.nested_default_fields + [
        'title', "collection", 'jpeg_400', 'jpeg_800', 'jpeg_1920'
    ]
    name = 'images'
    model = get_image_model()

    @method_decorator(cache_page(60*60))
    def list(self, request, format=None):
        return super().list(request, format)


api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
