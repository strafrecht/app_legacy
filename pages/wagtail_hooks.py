from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler, InlineEntityElementHandler
from wagtail.core import hooks
from draftjs_exporter.dom import DOM
from pages.models import People, NewsArticlePage, NodeAdmin, Events, Sessions

@hooks.register('register_rich_text_features')
def register_code_styling(features):
    feature_name = "code"
    type_ = "CODE"
    tag = "code"

    control = {
        "type": type_,
        "label": "</>",
        "description": "Code"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)

@hooks.register('register_rich_text_features')
def register_sidebar_feature(features):
    feature_name = "sidebar"
    type_ = "Sidebar"
    tag = "div"

    control = {
        "type": type_,
        "label": "Sidebar",
        "description": "Sidebar",
        "style": {
            "display": "flex",
            "border": "1px solid red",
        }
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": ".sidebar .sidebar-general"
                    }
               }
            }
        }
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)
                    

@hooks.register('register_rich_text_features')
def register_sidebar_general_feature(features):
    features.default_features.append('sidebar_general')
    """
    Registering the '<sidebar_general>' feature
    """
    feature_name = 'sidebar_general'
    type_ = 'SIDEBAR_GENERAL'

    control = {
        'type': type_,
        'label': '🏛️',
        'description': 'Sidebar General',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/sidebar_general.js'],
            css={'all': ['sidebar_general.css']}
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        'from_database_format': {'span[data-sidebar-general]': SidebarGeneralEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: sidebar_general_entity_decorator}},
    })

def sidebar_general_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the STOCK entities into a span tag.
    """
    return DOM.create_element('span', {
        'data-sidebar-general': props['sidebar-general'],
    }, props['children'])


class SidebarGeneralEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the span tag into a STOCK entity, with the right data.
    """
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        """
        Take the ``stock`` value from the ``data-stock`` HTML attribute.
        """
        return {
            'sidebar-general': attrs['data-sidebar-general'],
        }



@hooks.register('register_rich_text_features')
def register_stock_feature(features):
    features.default_features.append('stock')
    """
    Registering the `stock` feature, which uses the `STOCK` Draft.js entity type,
    and is stored as HTML with a `<span data-stock>` tag.
    """
    feature_name = 'stock'
    type_ = 'STOCK'

    control = {
        'type': type_,
        'label': '$',
        'description': 'Stock',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/stock.js'],
            css={'all': ['stock.css']}
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        'from_database_format': {'span[data-stock]': StockEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: stock_entity_decorator}},
    })

def stock_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the STOCK entities into a span tag.
    """
    return DOM.create_element('span', {
        'data-stock': props['stock'],
    }, props['children'])


class StockEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the span tag into a STOCK entity, with the right data.
    """
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        """
        Take the ``stock`` value from the ``data-stock`` HTML attribute.
        """
        return {
            'stock': attrs['data-stock'],
        }

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
