from django.urls import path
from . import views

urlpatterns = [
    # Existing endpoints
    path('api/qa/', views.qa, name='qa'),
    path('api/upload-doc/', views.upload_doc, name='upload_doc'),
    path('api/reload-doc/', views.reload_doc, name='reload_doc'),
    path('api/similar-doc/', views.similar_doc, name='similar_doc'),
    path('api/health-check/', views.health_check, name='health_check'),
    
    # News-related endpoints
    path('api/news/fetch-save/', views.fetch_and_save_political_news, name='fetch_save_news'),
    path('api/news/embed/', views.embed_news_articles, name='embed_news'),
    path('api/news/search/', views.search_political_news, name='search_news'),
    path('api/news/pipeline/', views.full_news_pipeline, name='news_pipeline'),
    path('api/news/stats/', views.news_stats, name='news_stats'),
]