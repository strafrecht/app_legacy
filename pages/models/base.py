# Wagtail
from wagtail.core import fields
from wagtail.core.models import Page
# Local
from .column_blocks import ColumnBlocks

class BasePage(Page):
    class Meta:
        abstract = True

    content = fields.StreamField(ColumnBlocks)
    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content')
    ]
