# Generated by Django 2.2.13 on 2020-11-02 22:41

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wesgarlockbase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('footer_content', models.TextField()),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_logo', to='wagtailimages.Image')),
                ('navigation', models.ManyToManyField(to='wagtailcore.Page')),
                ('site', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_content', to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('icon', models.CharField(blank=True, max_length=20, null=True)),
                ('site', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_media', to='wesgarlockbase.SiteContent')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
