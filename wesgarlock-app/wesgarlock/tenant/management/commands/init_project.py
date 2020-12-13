from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand
from wagtail.core.models import (
    Collection, Group, GroupCollectionPermission, GroupPagePermission, Page,
    PAGE_PERMISSION_TYPES, Site
)
from wagtail.images import get_image_model

from wesgarlock.base.models import Color, HomePage, SiteColor, SiteContent
from wesgarlock.blog.models import BlogIndexPage, BlogPage
from wesgarlock.tenant.constants import SITE_OWNER_GROUP_NAME


class Command(BaseCommand):
    help = 'Setup Project Requirements'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name=SITE_OWNER_GROUP_NAME
        )
        permissions = [
            "add_logentry",
            "change_logentry",
            "delete_logentry",
            "view_logentry",
            "add_group",
            "change_group",
            "delete_group",
            "view_group",
            "add_permission",
            "change_permission",
            "delete_permission",
            "view_permission",
            "add_token",
            "change_token",
            "delete_token",
            "view_token",
            "add_tokenproxy",
            "change_tokenproxy",
            "delete_tokenproxy",
            "view_tokenproxy",
            "add_contenttype",
            "change_contenttype",
            "delete_contenttype",
            "view_contenttype",
            "add_session",
            "change_session",
            "delete_session",
            "view_session",
            "add_tag",
            "change_tag",
            "delete_tag",
            "view_tag",
            "add_taggeditem",
            "change_taggeditem",
            "delete_taggeditem",
            "view_taggeditem",
            "access_admin",
            "add_collection",
            "change_collection",
            "delete_collection",
            "view_collection",
            "add_collectionviewrestriction",
            "change_collectionviewrestriction",
            "delete_collectionviewrestriction",
            "view_collectionviewrestriction",
            "add_groupapprovaltask",
            "change_groupapprovaltask",
            "delete_groupapprovaltask",
            "view_groupapprovaltask",
            "add_groupcollectionpermission",
            "change_groupcollectionpermission",
            "delete_groupcollectionpermission",
            "view_groupcollectionpermission",
            "add_grouppagepermission",
            "change_grouppagepermission",
            "delete_grouppagepermission",
            "view_grouppagepermission",
            "add_locale",
            "change_locale",
            "delete_locale",
            "view_locale",
            "add_page",
            "change_page",
            "delete_page",
            "view_page",
            "add_pagelogentry",
            "change_pagelogentry",
            "delete_pagelogentry",
            "view_pagelogentry",
            "add_pagerevision",
            "change_pagerevision",
            "delete_pagerevision",
            "view_pagerevision",
            "add_pageviewrestriction",
            "change_pageviewrestriction",
            "delete_pageviewrestriction",
            "view_pageviewrestriction",
            "add_task",
            "change_task",
            "delete_task",
            "view_task",
            "add_taskstate",
            "change_taskstate",
            "delete_taskstate",
            "view_taskstate",
            "add_workflow",
            "change_workflow",
            "delete_workflow",
            "view_workflow",
            "add_workflowpage",
            "change_workflowpage",
            "delete_workflowpage",
            "view_workflowpage",
            "add_workflowstate",
            "change_workflowstate",
            "delete_workflowstate",
            "view_workflowstate",
            "add_workflowtask",
            "change_workflowtask",
            "delete_workflowtask",
            "view_workflowtask",
            "add_embed",
            "change_embed",
            "delete_embed",
            "view_embed",
            "add_formsubmission",
            "change_formsubmission",
            "delete_formsubmission",
            "view_formsubmission",
            "add_rendition",
            "change_rendition",
            "delete_rendition",
            "view_rendition",
            "add_redirect",
            "change_redirect",
            "delete_redirect",
            "view_redirect",
            "add_query",
            "change_query",
            "delete_query",
            "view_query",
            "add_querydailyhits",
            "change_querydailyhits",
            "delete_querydailyhits",
            "view_querydailyhits",
            "add_userprofile",
            "change_userprofile",
            "delete_userprofile",
            "view_userprofile",
            "add_homepage",
            "change_homepage",
            "delete_homepage",
            "view_homepage",
            "add_sitecontent",
            "change_sitecontent",
            "delete_sitecontent",
            "view_sitecontent",
            "add_socialmedia",
            "change_socialmedia",
            "delete_socialmedia",
            "view_socialmedia",
            "add_user",
            "change_user",
            "delete_user",
            "view_user",
            "add_blogindexpage",
            "change_blogindexpage",
            "delete_blogindexpage",
            "view_blogindexpage",
            "add_blogpage",
            "change_blogpage",
            "delete_blogpage",
            "view_blogpage",
            "add_blogpagetag",
            "change_blogpagetag",
            "delete_blogpagetag",
            "view_blogpagetag",
            "add_sitecolor",
            "change_sitecolor",
            "delete_sitecolor",
            "view_sitecolor",
            "add_messagethread",
            "change_messagethread",
            "delete_messagethread",
            "view_messagethread",
        ]

        image_permissions = [
            "add_image",
            "change_image",
            "delete_image",
            "view_image",
            "add_uploadedimage",
            "change_uploadedimage",
            "delete_uploadedimage",
            "view_uploadedimage",
        ]

        document_permissions = [
            "add_document",
            "change_document",
            "delete_document",
            "view_document",
        ]

        group.permissions.set(Permission.objects.filter(codename__in=permissions + image_permissions + document_permissions))
        root_page = Page.objects.filter(depth=1).first()
        if created:
            collection = Collection.objects.filter(depth=1).first()
            [GroupPagePermission.objects.create(group=group, page=root_page, permission_type=permission[0]) for permission in PAGE_PERMISSION_TYPES]
            [GroupCollectionPermission.objects.create(group=group, collection=collection, permission=Permission.objects.get(codename=permission)) for permission in image_permissions + document_permissions]
        
        #create or get logo
        default_logo_path = finders.find(settings.BASE_DEFAULT_LOGO)
        logo = save_related_image("Default Logo", default_logo_path)
        #create or get hero
        default_hero_image = finders.find(settings.BASE_DEFAULT_HERO_IMAGE)
        hero_image = save_related_image("About Image", default_hero_image)
        #create or get about
        default_about_image = finders.find(settings.BASE_DEFAULT_ABOUT_IMAGE)
        about_image = save_related_image("About Image", default_about_image)
        #create or get og
        default_og_image = finders.find(settings.BASE_DEFAULT_OG_IMAGE)
        og_image = save_related_image("OG Image", default_og_image)

        site = Site.objects.filter(is_default_site=True).first()
        site_content, created = SiteContent.objects.get_or_create(
            site=site,
            defaults=dict(
                logo=logo,
                footer_content="Ipsum Lorem"
            )
        )
        if created:
            child = HomePage.objects.filter(title="Default Home Page").first()
            if not child:
                child = root_page.add_child(
                    instance=HomePage(
                        title="Default Home Page",
                        description="Ipsum Lorem",
                        about_me="Ipsum Lorem",
                        meta_description="Ipsum Lorem",
                        og_description="Ipsum Lorem",
                        hero_image=hero_image,
                        about_image=about_image,
                        og_image=og_image,
                    )
                )

            site.root_page = child
            site.save()

            site_color_fixture = [
                dict(
                    js_name="primary",
                    site=site_content,
                    colors=[
                        dict(
                            type=Color.TYPE.MAIN,
                            hex_color="#0D3B66"
                        ),
                    ]
                ),
                dict(
                    js_name="secondary",
                    site=site_content,
                    colors=[
                        dict(
                            type=Color.TYPE.MAIN,
                            hex_color="#0D3B66"
                        ),
                    ]
                ),
                dict(
                    js_name="common",
                    site=site_content,
                    colors=[
                        dict(
                            type=Color.TYPE.BLACK,
                            hex_color="#0D3B66"
                        ),
                        dict(
                            type=Color.TYPE.DARKBLACK,
                            hex_color="#0D3B66"
                        ),
                    ]
                ),
                dict(
                    js_name="background",
                    site=site_content,
                    colors=[
                        dict(
                            type=Color.TYPE.MAIN,
                            hex_color="#0D3B66"
                        ),
                    ]
                ),
                dict(
                    js_name="warning",
                    site=site_content,
                    colors=[
                        dict(
                            type=Color.TYPE.MAIN,
                            hex_color="#0D3B66"
                        ),
                    ]
                )
            ]

            for fixture in site_color_fixture:
                colors = fixture.pop("colors")
                site_color = SiteColor.objects.create(**fixture)
                for color in colors:
                    Color.objects.create(site_color=site_color, **color)

        Collection.objects.get_or_create(
            name="Public"
        )

        print("init project ran")


def save_related_image(title, path):
    Image = get_image_model()
    image = Image.objects.filter(title=title).first()
    if not image:
        with open(path, 'rb') as _file:
            file_data = File(_file)
            image = Image(title=title)
            image.file.save(
                name=image.title,
                content=file_data
            )
            image.save()
    return image
