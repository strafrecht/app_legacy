from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'user-answers', views.UserAnswerViewSet)
router.register(r'choices', views.ChoiceViewSet)

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('bt', views.index_bt, name='index_bt'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/question/<int:question_id>/', views.category_question, name='category_question'),
    path('category/<int:category_id>/summary/', views.category_summary, name='category_summary'),

    path('scrape/', views.scrape, name='scrape'),
    path('exams/', views.exams, name='exams'),
    path('search/wiki/', views.search_wiki, name='search_wiki'),
    path('search/wiki/<str:query>', views.search_wiki, name='search_wiki'),

    path('api/exams', views.api_exams, name='api_exams'),

    path('add_question/', views.add_question, name='add_question'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/category_tree', views.get_categories_tree, name='get_category_tree'),
    # path('api/', include(router.urls)),
]
