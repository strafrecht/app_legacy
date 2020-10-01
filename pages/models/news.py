from django.db import models
from django.contrib.auth.models import User
from itertools import groupby
import datetime

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.models import Document
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from pages.models import WebsitePage

#class NewsIndexPage(Page):

class NewsArticleIndexPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        news_article_pages = NewsArticlePage.objects.filter(live=True).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(news_article_pages, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        return context

class NewsArticlePage(WebsitePage):
    print("HERE")
    def get_context(self, request):
        print("HERE")
        print(request)
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

    
class NewsNewsletterPage(WebsitePage):
    def get_context(self, request):
        context = super().get_context(request)
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

        if d.month in [4,5,6,7,8,9]:
            title = "SS-{}".format(d.year)
            return {"title": title, "year": d.year}
        else:
            if d.month in [1,2,3]:
                title = "WS-{}".format(d.year-1)
                return {"title": title, "year": d.year-1}
            else:
                title = "WS-{}".format(d.year)
                return {"title": title, "year": d.year}

class NewsEvaluationIndexPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        news_evaluation_pages = NewsEvaluationPage.objects.filter(live=True).order_by('-date')

        years = []
        keys = []

        for key, group in groupby(news_evaluation_pages, lambda x: x.date.year):
            years.append({"year": key, "articles": list(group)})
            keys.append(key)

        context['groups'] = years
        return context

class NewsEvaluationPage(WebsitePage):
    def author_name(self):
        "ERROR"
        #return "{} {}".format(self.author.first_name, self.author.last_name)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Evaluation information"),
        FieldPanel('body', classname='full'),
        InlinePanel('sidebar_placements', label='Sidebar'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]
