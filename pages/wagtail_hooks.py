from django.utils.html import format_html
from django.templatetags.static import static
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler, InlineEntityElementHandler
from wagtail.core import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from pages.models import People, NodeAdmin, Events, Sessions, Exams
from wagtailpolls.models import Poll

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

class PollsModelAdmin(ModelAdmin):
    model = Poll
    menu_label = 'Abstimmungen'
    menu_icon = 'group'
    menu_order= 200
    #list_display = ('name', 'speaker', 'date')

class ExamsModelAdmin(ModelAdmin):
    model = Exams
    menu_label = 'Klausurdatenbank'
    menu_icon = 'group'
    menu_order= 200

modeladmin_register(NodeAdmin)
modeladmin_register(PeopleModelAdmin)
modeladmin_register(EventsModelAdmin)
modeladmin_register(SessionsModelAdmin)
modeladmin_register(PollsModelAdmin)
modeladmin_register(ExamsModelAdmin)

# pages/news/polls/poll-eval/sessions/events/people/newsletter email/

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/columns.css")
    )

@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
  for item in menu_items: print("XXX: {}".format(item.name))
  menu_items[:] = [item for item in menu_items if item.name not in ['snippets', 'images', 'documents', 'categories', 'contacts', 'Polls']]

@hooks.register('register_rich_text_features')
def register_roofline_feature(features):
    feature_name = 'roofline'
    type_ = 'roofline'

    control = {
        'type': type_,
        'label': '⛅',
        'description': 'Dachzeile',
        'element': 'p',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['base.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=roofline]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'p', 'props': {'class': 'roofline'}}}},
    })

    features.default_features.append('roofline')

@hooks.register('register_rich_text_features')
def register_revised_label_feature(features):
    feature_name = 'revised_label'
    type_ = 'revised_label'

    control = {
        'type': type_,
        'label': '♻️',        
        'description': 'Überarbeitet Label',        
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['base.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=label revised]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'label revised'}}}},
    })

    features.default_features.append('revised_label')

@hooks.register('register_rich_text_features')
def register_new_label_feature(features):
    feature_name = 'new_label'
    type_ = 'new_label'

    control = {
        'type': type_,
        'label': '☝️',        
        'description': 'Neu Label',        
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control, css={'all': ['base.css']})
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=label new]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'label new'}}}},
    })

    features.default_features.append('new_label')
