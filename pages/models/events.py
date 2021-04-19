from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Collection
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

class EventsIndexPage(RoutablePageMixin, Page):
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cover_caption = models.CharField(max_length=255, blank=True, null=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('cover'),
        FieldPanel('cover_caption'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        events = Events.objects.all()
        context['events'] = events
        return context

    @route('(?P<event>\d+)/$', name="event")
    def event_page(self, request, event):
        context = super().get_context(request)
        event = Events.objects.get(id=event)
        context['event'] = event
        return render(request, "pages/event_page.html", {'event': event})

#class EventTags(TaggedItemBase):
#    content_object = ParentalKey(
#        'pages.Events', related_name='tagged_items', on_delete=models.CASCADE
#    )
    
@register_snippet
class Events(models.Model):
    EVENT_TYPE_CHOICES = [
        ('tacheles', 'Tacheles'),
        ('sonstige', 'Sonstige')
    ]

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    date = models.DateTimeField()
    #tags = ClusterTaggableManager(through=EventTags, blank=True)
    poster_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    poster_pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    speaker = models.CharField(max_length=255, null=True, blank=True)
    youtube_link = models.CharField(max_length=500, null=True, blank=True)
    newsletter_link = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(
        choices=EVENT_TYPE_CHOICES,
        default='tacheles',
        max_length=255,
        blank=True
    )
    description = RichTextField(blank=True)
    speaker_description = RichTextField(blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name', classname="col-12"),
            FieldPanel('subtitle', classname="col-12"),
        ], "Event"),
        MultiFieldPanel([
            FieldPanel('date', classname="col-12"),
            FieldPanel('type', classname="col-12"),
            FieldPanel('description', classname="col-12"),
        ], "Info"),
        MultiFieldPanel([
            ImageChooserPanel('poster_image', classname="col-12"),
            DocumentChooserPanel('poster_pdf', classname="col-12"),
        ], "Poster"),
        MultiFieldPanel([
            FieldPanel('speaker', classname="col-12"),
            FieldPanel('speaker_description', classname="col-12"),
        ], "Speaker"),
        MultiFieldPanel([
            FieldPanel('youtube_link', classname="col-12"),
            FieldPanel('newsletter_link', classname="col-12"),
        ], "Links"),
        MultiFieldPanel([
            FieldPanel('location', classname="col-12"),
            FieldPanel('lat', classname="col-6"),
            FieldPanel('lon', classname="col-6"),
        ], "Location"),
    ]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('speaker'),
    ]

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition('fill-120x120').img_tag()
        except:
            return ''

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Event'
        verbose_name = 'Events'
