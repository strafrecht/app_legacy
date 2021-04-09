from wiki.models import Article, ArticleRevision
from .models import Submission, QuestionVersion, Question
from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin
from treemodeladmin.options import TreeModelAdmin


# @modeladmin_register
class SubmissionAdmin(TreeModelAdmin):
    menu_label = 'Einreichungen'
    model = Submission
    parent_field = 'question_version'
    list_display = ('submitted_by', 'reviewed_by', 'article_revision', 'question_version', 'status', 'message')


# @modeladmin_register
class QuestionVersionAdmin(TreeModelAdmin):
    menu_label = 'Fragen'
    menu_icon = 'list-ul'
    model = QuestionVersion
    parent_field = 'question'
    child_field = 'submission_set'
    child_model_admin = SubmissionAdmin
    list_display = ('question', 'title', 'description', 'categories', 'approved', 'user')


@modeladmin_register
class QuestionAdmin(TreeModelAdmin):
    menu_label = 'Fragen Admin'
    menu_icon = 'list-ul'
    model = Question
    child_field = 'questionversion_set'
    child_model_admin = QuestionVersionAdmin
    list_display = ('filepath', 'slug')

"""
@modeladmin_register
class ArticleAdmin(ModelAdmin):
    model = ArticleRevision
    menu_label = "Wiki Articles"
    menu_icon = "placeholder"
    # menu_order = 290
    # add_to_settings_menu = False
    # exclude_from_explorer = False
    list_display = ('created', 'modified')
    # search_fields = ("email", "full_name",)
"""