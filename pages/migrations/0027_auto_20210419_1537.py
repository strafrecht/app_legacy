# Generated by Django 3.1.8 on 2021-04-19 15:37

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail_color_panel.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('pages', '0026_auto_20210408_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='poster',
            new_name='posterimage',
        ),
        migrations.AddField(
            model_name='events',
            name='newsletter',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='posterpdf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document'),
        ),
        migrations.AddField(
            model_name='events',
            name='youtube',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='sidebarpage',
            name='content',
            field=wagtail.core.fields.StreamField([('column_2_1', wagtail.core.blocks.StructBlock([('column_0', wagtail.core.blocks.StreamBlock([('text', wagtail.core.blocks.RichTextBlock()), ('sidebar_title', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_simple', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_border', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_image_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('sidebar_calendar_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('calendar', wagtail.core.blocks.DateBlock(format='%Y-%m-%d'))])), ('sidebar_header', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('color', wagtail_color_panel.blocks.NativeColorBlock('color', default='#333d44')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('content', wagtail.core.blocks.RichTextBlock(required=False))])), ('sidebar_poll', wagtail.core.blocks.StructBlock([])), ('sidebar_subscribe', wagtail.core.blocks.StructBlock([])), ('sidebar_event', wagtail.core.blocks.StructBlock([])), ('home_news_block', wagtail.core.blocks.StructBlock([])), ('news_list_all', wagtail.core.blocks.StructBlock([])), ('events_list_all', wagtail.core.blocks.StructBlock([])), ('home_jurcoach_block', wagtail.core.blocks.StructBlock([])), ('news_newsletter_block', wagtail.core.blocks.StructBlock([]))])), ('column_1', wagtail.core.blocks.StreamBlock([('text', wagtail.core.blocks.RichTextBlock()), ('sidebar_title', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_simple', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_border', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock())])), ('sidebar_image_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('sidebar_calendar_text', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock()), ('calendar', wagtail.core.blocks.DateBlock(format='%Y-%m-%d'))])), ('sidebar_header', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('color', wagtail_color_panel.blocks.NativeColorBlock('color', default='#333d44')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('content', wagtail.core.blocks.RichTextBlock(required=False))])), ('sidebar_poll', wagtail.core.blocks.StructBlock([])), ('sidebar_subscribe', wagtail.core.blocks.StructBlock([])), ('sidebar_event', wagtail.core.blocks.StructBlock([])), ('home_news_block', wagtail.core.blocks.StructBlock([])), ('news_list_all', wagtail.core.blocks.StructBlock([])), ('events_list_all', wagtail.core.blocks.StructBlock([])), ('home_jurcoach_block', wagtail.core.blocks.StructBlock([])), ('news_newsletter_block', wagtail.core.blocks.StructBlock([]))]))], grid_width=12, group='Columns', template='blocks/columnsblock.html'))]),
        ),
    ]