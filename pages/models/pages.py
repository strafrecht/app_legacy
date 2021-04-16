from django.db import models
from django.contrib.auth.models import User

from itertools import groupby
import datetime

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.documents.models import Document
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core import blocks
from wagtail.core import fields
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.blocks import NativeColorBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtailpolls.models import Poll
from wagtailpolls.edit_handlers import PollChooserPanel
from wagtailcolumnblocks.blocks import ColumnsBlock
from .events import Events
from news.models import NewsItem


# from pages.models import NewsArticleIndexPage

class WebsiteIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        news_articles = WebsitePage.objects.filter(content_type__model='newsarticlepage').order_by(
            '-first_published_at')[0:2]
        context['articles'] = news_articles
        return context


class WebsitePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebsitePage', related_name='tagged_items', on_delete=models.CASCADE
    )


class WebsitePage(Page):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    date = models.DateField('Post date')
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    intro = models.CharField(max_length=250, blank=True, null=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=WebsitePageTag, blank=True)
    sidebar = RichTextField(blank=True)
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cover_caption = models.CharField(max_length=255, blank=True, null=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        ImageChooserPanel('cover'),
        FieldPanel('cover_caption'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Website information"),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    def get_absolute_url(self):
        return self.get_url()


class WebsitePageGalleryImage(Orderable):
    page = ParentalKey(WebsitePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


# Widgets
class HomeNewsBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_block.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['articles'] = NewsItem.objects.all()[0:4]
        return ctx

class EventsListAll(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/events_list.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['events'] = Events.objects.all()
        return ctx

class NewsListAll(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_list.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['articles'] = NewsItem.objects.all()
        return ctx


class HomeJurcoachBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/home_jurcoach.html'


class NewsNewsletterBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_newsletter.html'

    def get_context(self, *a, **kw):
        context = super().get_context(*a, **kw)
        newsletters = Document.objects.filter(tags__name='newsletter')
        semesters = []
        keys = []

        for key, group in groupby(newsletters, get_semester):
            semesters.append({"semester": key["title"], "year": key["year"], "newsletters": list(group)})

        semesters = sorted(semesters, key=lambda x: x['year'], reverse=True)
        context['semesters'] = semesters
        return context


def get_semester(doc):
    date_string = doc.filename.split("Lehrstuhlnewsletter20vom20")[-1].split(".pdf")[0]
    d = datetime.datetime.strptime(date_string, '%d.%m.%Y')

    if d.month in [4, 5, 6, 7, 8, 9]:
        title = "SS {}".format(d.year)
        return {"title": title, "year": d.year}
    else:
        if d.month in [1, 2, 3]:
            title = "WS {}".format(d.year - 1)
            return {"title": title, "year": d.year - 1}
        else:
            title = "WS {}".format(d.year)
            return {"title": title, "year": d.year}


# Sidebars
class SidebarTitleBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/sidebar/title.html'


class SidebarSimpleBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/sidebar/simple.html'


class SidebarBorderBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/sidebar/border.html'


class SidebarImageTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'blocks/sidebar/image_text.html'


class SidebarCalendarTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()
    calendar = blocks.DateBlock(format="%Y-%m-%d")

    class Meta:
        template = 'blocks/sidebar/calendar_text.html'


class SidebarHeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    color = NativeColorBlock('color', default="#333d44")
    image = ImageChooserBlock()
    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'blocks/sidebar/header.html'


class SidebarPollBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/poll.html'


class SidebarSubscribeBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/subscribe.html'


class SidebarEventBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/sidebar/event.html'


class ContentBlocks(blocks.StreamBlock):
    """
    The blocks you want to allow within each ColumnBlocks column.
    """

    text = blocks.RichTextBlock()

    sidebar_title = SidebarTitleBlock()
    sidebar_simple = SidebarSimpleBlock()
    sidebar_border = SidebarBorderBlock()
    sidebar_image_text = SidebarImageTextBlock()
    sidebar_calendar_text = SidebarCalendarTextBlock()
    sidebar_header = SidebarHeaderBlock()
    sidebar_poll = SidebarPollBlock()
    sidebar_subscribe = SidebarSubscribeBlock()
    sidebar_event = SidebarEventBlock()

    home_news_block = HomeNewsBlock()
    news_list_all = NewsListAll()
    events_list_all = EventsListAll()
    home_jurcoach_block = HomeJurcoachBlock()
    news_newsletter_block = NewsNewsletterBlock()


class ColumnBlocks(blocks.StreamBlock):
    """
    All the root level blocks you can use
    """
    column_2_1 = ColumnsBlock(
        # Blocks you want to allow within each column
        ContentBlocks(),
        # Two columns in admin, first twice as wide as the second
        ratios=(2, 1),
        # Used for grouping related fields in the streamfield field picker
        group="Columns",
        # 12 column frontend grid (this is the default, so can be omitted)
        grid_width=12,
        # Override the frontend template
        template='blocks/columnsblock.html',
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
        return context


class SidebarPage(Page):
    content = fields.StreamField(ColumnBlocks)
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cover_caption = models.CharField(max_length=255, blank=True, null=True)
    poll = models.ForeignKey(
        'wagtailpolls.Poll',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    content_panels = [
        FieldPanel('title'),
        ImageChooserPanel('cover'),
        FieldPanel('cover_caption'),
        PollChooserPanel('poll'),
        StreamFieldPanel('content')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # news_articles = WebsitePage.objects.filter(content_type__model='newsarticlepage').order_by('-first_published_at')[0:2]
        # context['articles'] = news_articles
        # context['poll'] = Poll.objects.first()
        context['request'] = request
        return context

    def get_absolute_url(self):
        return self.get_url()
