# Generated by Django 3.1.8 on 2021-05-28 14:13

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail_color_panel.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailmenus', '0023_remove_use_specific'),
        ('news', '0003_auto_20210521_1354'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('pages', '0042_homepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='basepage_ptr',
        ),
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([('content', wagtail.core.blocks.StreamBlock([('richtext', wagtail.core.blocks.RichTextBlock())]))], default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, default=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='sidebar',
            field=wagtail.core.fields.StreamField([('sidebar', wagtail.core.blocks.StreamBlock([('sidebar_title', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_simple', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_border', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_image_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('sidebar_calendar_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('calendar', wagtail.core.blocks.DateBlock(format='%Y-%m-%d'))])), ('sidebar_header', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('color', wagtail_color_panel.blocks.NativeColorBlock('color', default='#333d44')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('content', wagtail.core.blocks.RichTextBlock(required=False))])), ('sidebar_poll', wagtail.core.blocks.StructBlock([])), ('sidebar_subscribe', wagtail.core.blocks.StructBlock([])), ('sidebar_event', wagtail.core.blocks.StructBlock([]))]))], default=False),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BasePage',
        ),
    ]
