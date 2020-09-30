from django.db import models
from wagtail.core.models import Page
from pages.models import Node

class WikiIndexPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        root = Node.objects.first()
        context['categories'] = root.get_descendants()
        return context

class WikiPage(Page):
    node = models.ForeignKey(
        'pages.Node',
        on_delete=models.CASCADE,
    )
