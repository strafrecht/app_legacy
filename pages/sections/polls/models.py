from django.db import models
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from pages.models import WebsitePage
from poll.models import Poll

#class NewsIndexPage(Page):

class PollIndexPage(WebsitePage):
    def get_context(self, request):
        context = super().get_context(request)
        poll_review_pages = self.get_children().live().order_by('-first_published_at')
        context['reviews'] = poll_review_pages
        return context

class PollReviewPage(WebsitePage):
    poll = models.ForeignKey(
        Poll,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['poll'] = self
        return context

    def author_name(self):
        return "{} {}".format(self.author.first_name, self.author.last_name)

    content_panels = Page.content_panels + [
        FieldPanel('poll'),
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Article information"),
        FieldPanel('body', classname='full'),
        InlinePanel('sidebar_placements', label='Sidebar'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]

    
