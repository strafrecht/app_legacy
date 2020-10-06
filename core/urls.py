from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/question/<int:question_id>/', views.category_question, name='category_question'),
    path('category/<int:category_id>/summary/', views.category_summary, name='category_summary'),

    path('scrape/', views.scrape, name='scrape'),
    path('exams/', views.exams, name='exams')
]
