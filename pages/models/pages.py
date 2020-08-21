from django.db import models
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

#from pages.models import NewsArticleIndexPage

class WebsiteIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        news_articles = WebsitePage.objects.filter(content_type__model='newsarticlepage').order_by('-first_published_at')[0:2]
        context['articles'] = news_articles
        return context

class WebsitePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'WebsitePage', related_name='tagged_items', on_delete=models.CASCADE
    )

class WebsitePageSidebarPlacement(Orderable, models.Model):
    page = ParentalKey('pages.WebsitePage', on_delete=models.CASCADE, related_name='sidebar_placements')
    sidebar = models.ForeignKey('pages.Sidebar', on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = "advert placement"
        verbose_name_plural = "advert placements"
        
    panels = [
        SnippetChooserPanel('sidebar'),
    ]

    def __str__(self):
        return self.page.title + " -> sidebar"

class WebsitePage(Page):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    date = models.DateField('Post date')
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    intro = models.CharField(max_length=250, blank=True, null=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=WebsitePageTag, blank=True)

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
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Website information"),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]

    sidebar_content_panels = [
        InlinePanel('sidebar_placements', label='Sidebar'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_content_panels, heading='Sidebar content'),
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

@register_snippet
class Sidebar(index.Indexed, models.Model):
    SIDEBAR_CHOICES = [('standard', 'Standard'),('poll', 'Poll')]
    name = models.CharField(max_length=100)
    text = RichTextField(blank=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    type = models.CharField(
        choices=SIDEBAR_CHOICES,
        default='standard',
        max_length=255
    )
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-updated_at"]
