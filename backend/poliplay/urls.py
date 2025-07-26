from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),
     path('api/quize/', include('quize.urls')),
    # path('api/news', include('Dnews.urls')),
]