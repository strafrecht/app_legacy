# Wagtail
from wagtail.core import blocks, fields
# 3rd Party
from wagtailcolumnblocks.blocks import ColumnsBlock
# Local
from pages.models.base import BasePage
from .sidebar import (
    SidebarTitleBlock,
    SidebarSimpleBlock,
    SidebarBorderBlock,
    SidebarImageTextBlock,
    SidebarCalendarTextBlock,
    SidebarHeaderBlock,
    SidebarPollBlock,
    SidebarSubscribeBlock,
    SidebarEventBlock
)
#from pages.sections.news.blocks import HomeNewsBlock
#from pages.sections.home.blocks import HomeJurcoachBlock
from pages.sections.news.blocks import NewsListAll
from pages.sections.news.blocks import NewsNewsletterBlock
#from pages.sections.events.blocks import EventsListAll

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

class PageMixin(BasePage):
    class Meta:
        abstract = True

    content = fields.StreamField(ColumnBlocks)
    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content')
    ]