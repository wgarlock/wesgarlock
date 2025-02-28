# Generated by Django 2.2.13 on 2020-11-02 22:46

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.core.fields
import wesgarlock.base.models._base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailimages', '0001_squashed_0021'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.core.fields.RichTextField(default='')),
                ('meta_description', models.CharField(blank=True, max_length=120, null=True)),
                ('og_description', models.CharField(blank=True, max_length=300, null=True)),
                ('date', models.DateField(verbose_name='Post date')),
                ('intro', models.CharField(blank=True, max_length=1000, null=True)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('og_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Blog Page',
                'verbose_name_plural': 'Blog Pages',
            },
            bases=(wesgarlock.base.models._base.BasePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='wesgarlockblog.BlogPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wesgarlockblog_blogpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='wesgarlockblog.BlogPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.core.fields.RichTextField(default='')),
                ('meta_description', models.CharField(blank=True, max_length=120, null=True)),
                ('og_description', models.CharField(blank=True, max_length=300, null=True)),
                ('og_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Blog Index Page',
                'verbose_name_plural': 'Blog Index Pages',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, wesgarlock.base.models._base.BasePageMixin, 'wagtailcore.page'),
        ),
    ]
