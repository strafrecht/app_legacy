from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler, InlineEntityElementHandler
from wagtail.core import hooks
from draftjs_exporter.dom import DOM
from pages.models import People, NewsArticlePage, NodeAdmin, Events, Sessions

class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'Personen'
    menu_icon = 'user'
    menu_order= 202
    list_display = ('status', 'last_name', 'first_name', 'role')

class EventsModelAdmin(ModelAdmin):
    model = Events
    menu_label = 'Events'
    menu_icon = 'site'
    menu_order= 201
    list_display = ('name', 'speaker', 'date')

class SessionsModelAdmin(ModelAdmin):
    model = Sessions
    menu_label = 'Lehrveranstaltungen'
    menu_icon = 'date'
    menu_order= 200
    list_display = ('name', 'speaker', 'date')

modeladmin_register(NodeAdmin)
modeladmin_register(PeopleModelAdmin)
modeladmin_register(EventsModelAdmin)
modeladmin_register(SessionsModelAdmin)

# pages/news/polls/poll-eval/sessions/events/people/newsletter email/
@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
  menu_items[:] = [item for item in menu_items if item.name not in ['snippets', 'images', 'documents', 'categories', 'contacts']]
