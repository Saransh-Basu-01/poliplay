from django.urls import path
from . import views

app_name = 'category_game'

urlpatterns = [
    # Categories
    path('categories/', views.QuizCategoriesView.as_view(), name='quiz_categories'),
    
    # Quiz management
    path('start/', views.StartQuizView.as_view(), name='start_quiz'),
    path('generate-questions/', views.GenerateQuizQuestionsView.as_view(), name='generate_questions'),
    path('topics/', views.get_available_topics, name='available_topics'),
    
    # Quiz sessions
    path('sessions/', views.QuizSessionView.as_view(), name='quiz_sessions'),
    path('sessions/<str:session_id>/', views.QuizSessionView.as_view(), name='quiz_session_detail'),
    path('sessions/<str:session_id>/complete/', views.CompleteQuizView.as_view(), name='complete_quiz'),
    
    # Answers
    path('submit-answer/', views.SubmitAnswerView.as_view(), name='submit_answer'),
    
    # Statistics
    path('stats/', views.quiz_stats, name='quiz_stats'),
]