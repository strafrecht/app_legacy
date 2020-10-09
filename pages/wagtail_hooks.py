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
def register_neu_feature(features):
    feature_name = 'neulabel'
    type_ = 'NEULABEL'
    tag = 'NEU'

    control = {
        'type': type_,
        'label': 'NEU',        
        'description': 'Neu-Label',        
        'style': {            
            'font-size': '75%',            
            'color': '#666'        
        }    
    }

    features.register_editor_plugin(        
        'draftail',
        feature_name,
        draftail_features.InlineStyleFeature(control)    
    )     

    db_conversion = {        
        'from_database_format': {'NEU': InlineStyleElementHandler(type_)},        'to_database_format': {'block_map': {type_: 'span class="label neu"'}},    
    }     

    features.register_converter_rule(
        'contentstate',
        feature_name,
        db_conversion
    )

    features.default_features.append('n')

@hooks.register('register_rich_text_features')
def register_ueberarbeitet_feature(features):
    feature_name = 'ueberarbeitetlabel'
    type_ = 'UEBERARBEITETLABEL'
    control = {
        'type': type_,
        'label': 'Überarbeitet',        
        'description': 'Überarbeitet-Label',        
        'style': {            
            'font-size': '75%',            
            'color': '#666'        
        }    
    }
    features.register_editor_plugin(        
        'draftail',
        feature_name,
        draftail_features.InlineStyleFeature(control)    
    )     
    db_conversion = {        
        'from_database_format': {
            'span[class="label ueberarbeitet"]':
                   InlineStyleElementHandler(type_)
        },        
        'to_database_format': {
            'style_map': {type_: 'span class="label ueberarbeitet"'}
        },    
    }     
    features.register_converter_rule(
        'contentstate',
        feature_name,
        db_conversion
    )

@hooks.register('register_rich_text_features')
def register_roofline_feature(features):
    feature_name = 'roofline'
    type_ = 'ROOFLINE'
    control = {
        'type': type_,
        'label': 'Dachzeile',        
        'description': 'Blaue Dachzeile',        
        'style': {            
            'font-size': '75%',            
            'color': '#666'        
        }    
    }
    features.register_editor_plugin(        
        'draftail',
        feature_name,
        draftail_features.InlineStyleFeature(control)    
    )     
    db_conversion = {        
        'from_database_format': {
            'p[class="roofline"]':
                   InlineStyleElementHandler(type_)
        },        
        'to_database_format': {
            'style_map': {type_: 'p class="roofline"'}
        },    
    }     
    features.register_converter_rule(
        'contentstate',
        feature_name,
        db_conversion
    )

@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'blockquote'
    type_ = 'blockquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'label': '❝',
        'description': 'Blockquote',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'blockquote',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {tag: BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: tag}},
    })

    features.default_features.append('blockquote')
