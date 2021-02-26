from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks

from .models import Question, QuestionVersion


class QuestionAdmin(ModelAdmin):
    model = Question
    menu_label = 'Fragen'
    menu_icon = 'folder'
    list_display = ('id', 'user')


class QuestionVersionAdmin(ModelAdmin):
    model = QuestionVersion
    menu_label = 'Fragen Versionen'
    menu_icon = 'folder'
    list_display = ('question', 'title', 'description', 'categories', 'approved', 'answers')


class MCTAdmin(ModelAdminGroup):
    menu_label = 'MCT'
    menu_icon = 'folder'
    items = (QuestionAdmin, QuestionVersionAdmin)


modeladmin_register(MCTAdmin)