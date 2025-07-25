from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
from .models import Question, Document
from .serializers import QuestionSerializer, QuestionRequestSerializer
from .services import rag_service  # Import from services instead of rag_service
import logging
import os

logger = logging.getLogger(__name__)

class LegalQAView(APIView):
    """
    Main endpoint for legal Q&A using RAG
    """
    def post(self, request):
        serializer = QuestionRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid request", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = serializer.validated_data['question']
        language = serializer.validated_data.get('language', 'en')
        
        try:
            # Check if RAG service is available
            if not rag_service:
                return Response(
                    {"error": "RAG service not available"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            # Get answer from RAG system
            answer = rag_service.ask_question(question)
            
            # Save to database
            question_obj = Question.objects.create(
                question_text=question,
                answer_text=answer,
                language=language
            )
            
            # Get similar documents for context
            similar_docs = rag_service.get_similar_documents(question)
            
            response_data = {
                "id": question_obj.id,
                "question": question,
                "answer": answer,
                "language": language,
                "similar_documents": similar_docs,
                "created_at": question_obj.created_at.isoformat()
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in LegalQAView: {str(e)}")
            return Response(
                {"error": "Internal server error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuestionHistoryView(APIView):
    """
    Get question history
    """
    def get(self, request):
        questions = Question.objects.all().order_by('-created_at')[:20]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    rag_status = "available" if rag_service else "unavailable"
    document_status = None
    
    if rag_service:
        try:
            document_status = rag_service.get_document_status()
        except Exception as e:
            logger.error(f"Error getting document status: {e}")
    
    return JsonResponse({
        "status": "healthy",
        "service": "Legal RAG API",
        "rag_service": rag_status,
        "document_status": document_status,
        "timestamp": "2025-07-25T08:07:00Z"
    })

@api_view(['POST'])
def search_documents(request):
    """Search for similar documents without generating an answer"""
    question = request.data.get('question', '')
    k = request.data.get('k', 4)
    
    if not question:
        return JsonResponse(
            {"error": "Question is required"},
            status=400
        )
    
    try:
        if not rag_service:
            return JsonResponse(
                {"error": "RAG service not available"},
                status=503
            )
            
        similar_docs = rag_service.get_similar_documents(question, k)
        return JsonResponse({
            "question": question,
            "documents": similar_docs,
            "count": len(similar_docs)
        })
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )

@api_view(['GET'])
def document_status(request):
    """Get document loading status"""
    if not rag_service:
        return JsonResponse({"error": "RAG service not available"}, status=503)
    
    try:
        status_info = rag_service.get_document_status()
        return JsonResponse(status_info)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['POST'])
def reload_documents(request):
    """Reload documents from data directory"""
    if not rag_service:
        return JsonResponse({"error": "RAG service not available"}, status=503)
    
    try:
        result = rag_service.reload_documents()
        return JsonResponse({"message": result})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

class DocumentUploadView(APIView):
    """Upload new documents"""
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        
        # Save file to data directory
        data_dir = os.path.join(settings.BASE_DIR, 'chatbot', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        file_path = os.path.join(data_dir, file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Save to database
        document = Document.objects.create(
            name=file.name,
            file_path=file_path,
            is_processed=False
        )
        
        return Response({
            "message": "File uploaded successfully",
            "document_id": document.id,
            "file_name": file.name
        })