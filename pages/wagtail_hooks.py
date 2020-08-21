from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from pages.models import People, NewsArticlePage, NodeAdmin, Events

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
    menu_icon = 'date'
    list_display = ('name', 'speaker', 'date')


class PeopleModelAdminGroup(ModelAdminGroup):
    menu_label = 'Institute'
    menu_icon = 'cog'
    menu_order= 200
    items = (ArticleModelAdmin, PeopleModelAdmin, EventsModelAdmin)

modeladmin_register(PeopleModelAdminGroup)
modeladmin_register(NodeAdmin)
