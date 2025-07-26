from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<str:name>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('quiz/submit/', views.QuizSubmitView.as_view(), name='quiz-submit'),
    path('quiz/stats/', views.quiz_stats, name='quiz-stats'),
]