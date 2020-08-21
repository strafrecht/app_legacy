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

#class NewsIndexPage(Page):

class NewsArticleIndexPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        news_article_pages = NewsArticlePage.objects.filter(live=True).order_by('date')
        context['articles'] = news_article_pages
        return context

class NewsArticlePage(WebsitePage):
    def author_name(self):
        "ERROR"
        #return "{} {}".format(self.author.first_name, self.author.last_name)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Article information"),
        FieldPanel('body', classname='full'),
        InlinePanel('sidebar_placements', label='Sidebar'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]

    
