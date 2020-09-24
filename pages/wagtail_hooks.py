from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler, InlineEntityElementHandler
from wagtail.core import hooks
from draftjs_exporter.dom import DOM
from pages.models import People, NewsArticlePage, NodeAdmin, Events, Sessions

class ArticleModelAdmin(ModelAdmin):
    model = NewsArticlePage
    menu_label = 'Articles'
    menu_icon = 'doc-full'
    list_display = ('title', 'author', 'date')

class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'People'
    menu_icon = 'user'
    list_display = ('status', 'last_name', 'first_name', 'role')

class EventsModelAdmin(ModelAdmin):
    model = Events
    menu_label = 'Events'
    menu_icon = 'site'
    list_display = ('name', 'speaker', 'date')

class SessionsModelAdmin(ModelAdmin):
    model = Sessions
    menu_label = 'Sessions'
    menu_icon = 'date'
    list_display = ('name', 'speaker', 'date')

class PeopleModelAdminGroup(ModelAdminGroup):
    menu_label = 'Institute'
    menu_icon = 'cog'
    menu_order= 200
    items = (ArticleModelAdmin, PeopleModelAdmin, SessionsModelAdmin, EventsModelAdmin)

modeladmin_register(PeopleModelAdminGroup)
modeladmin_register(NodeAdmin)
