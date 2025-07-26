from django.urls import path
from .views import (
    LegalQAView, QuestionHistoryView, health_check, search_documents,
    document_status, reload_documents, DocumentUploadView,fetch_government_pdfs
)
# from govs_pdfs import fetch

urlpatterns = [
    path('chat/', LegalQAView.as_view(), name='legal_qa'),
    path('history/', QuestionHistoryView.as_view(), name='question_history'),
    path('health/', health_check, name='health_check'),
    path('search/', search_documents, name='search_documents'),
    path('documents/status/', document_status, name='document_status'),
    path('documents/reload/', reload_documents, name='reload_documents'),
    path('documents/upload/', DocumentUploadView.as_view(), name='document_upload'),
    path('api/fetch-pdfs/', fetch_government_pdfs, name='fetch_pdfs'),
]