# Generated by Django 3.1.8 on 2021-05-28 14:05

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail_color_panel.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailmenus', '0023_remove_use_specific'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('news', '0003_auto_20210521_1354'),
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('pages', '0040_auto_20210528_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.core.fields.StreamField([('content', wagtail.core.blocks.StreamBlock([('richtext', wagtail.core.blocks.RichTextBlock())]))])),
                ('sidebar', wagtail.core.fields.StreamField([('sidebar', wagtail.core.blocks.StreamBlock([('sidebar_title', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_simple', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_border', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_image_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('sidebar_calendar_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('calendar', wagtail.core.blocks.DateBlock(format='%Y-%m-%d'))])), ('sidebar_header', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('color', wagtail_color_panel.blocks.NativeColorBlock('color', default='#333d44')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('content', wagtail.core.blocks.RichTextBlock(required=False))])), ('sidebar_poll', wagtail.core.blocks.StructBlock([])), ('sidebar_subscribe', wagtail.core.blocks.StructBlock([])), ('sidebar_event', wagtail.core.blocks.StructBlock([]))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.DeleteModel(
            name='HomePage',
        ),
    ]