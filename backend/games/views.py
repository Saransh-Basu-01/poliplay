from rest_framework.views import APIView
import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Avg
from .models import QuizQuestion, QuizSession, UserAnswer, QuizCategory
from .serializers import (
    QuizQuestionSerializer, QuizQuestionWithAnswerSerializer,
    QuizSessionSerializer, UserAnswerSerializer, SubmitAnswerSerializer,
    GenerateQuestionSerializer, QuizCategorySerializer, StartQuizSerializer
)
from quize_service import quiz_generation_service
from chatbot.services import rag_service
import logging
import uuid
from datetime import timedelta

logger = logging.getLogger(__name__)

class QuizCategoriesView(APIView):
    """Get all quiz categories"""
    
    def get(self, request):
        categories = QuizCategory.objects.filter(is_active=True).annotate(
            questions_count=Count('questions', filter=models.Q(questions__is_active=True))
        )
        serializer = QuizCategorySerializer(categories, many=True)
        return Response(serializer.data)

class GenerateQuizQuestionsView(APIView):
    """Generate quiz questions using RAG model"""
    
    def post(self, request):
        serializer = GenerateQuestionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not rag_service:
            return Response(
                {"error": "Question generation service not available"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        topic = serializer.validated_data.get('topic', 'general knowledge')
        category_name = serializer.validated_data.get('category', 'General')
        difficulty = serializer.validated_data.get('difficulty', 'medium')
        count = serializer.validated_data.get('count', 5)
        
        generated_questions = []
        
        try:
            # Generate questions
            questions = quiz_generation_service.generate_multiple_questions(
                topic, count, difficulty, category_name
            )
            
            for question in questions:
                if question:
                    question_serializer = QuizQuestionSerializer(question)
                    generated_questions.append(question_serializer.data)
            
            return Response({
                "questions": generated_questions,
                "count": len(generated_questions),
                "topic": topic,
                "category": category_name,
                "difficulty": difficulty
            })
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return Response(
                {"error": "Failed to generate questions", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StartQuizView(APIView):
    """Start a new quiz session"""
    
    def post(self, request):
        serializer = StartQuizSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        category_id = serializer.validated_data.get('category_id')
        difficulty = serializer.validated_data.get('difficulty', 'medium')
        question_count = serializer.validated_data.get('question_count', 10)
        generate_new = serializer.validated_data.get('generate_new', False)
        topics = serializer.validated_data.get('topics', [])
        
        try:
            # Create quiz session
            session_id = str(uuid.uuid4())
            category = None
            
            if category_id:
                try:
                    category = QuizCategory.objects.get(id=category_id)
                except QuizCategory.DoesNotExist:
                    return Response(
                        {"error": "Category not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            quiz_session = QuizSession.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                category=category
            )
            
            # Get or generate questions
            questions = []
            
            if generate_new and topics:
                # Generate new questions using RAG
                category_name = category.name if category else "Generated"
                questions = quiz_generation_service.generate_multiple_questions(
                    topics, question_count, difficulty, category_name
                )
            else:
                # Get existing questions
                question_query = QuizQuestion.objects.filter(is_active=True)
                
                if category:
                    question_query = question_query.filter(category=category)
                
                if difficulty:
                    question_query = question_query.filter(difficulty=difficulty)
                
                questions = list(question_query.order_by('?')[:question_count])
            
            if not questions:
                return Response(
                    {"error": "No questions available for the selected criteria"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Serialize questions (without correct answers)
            question_serializer = QuizQuestionSerializer(questions, many=True)
            session_serializer = QuizSessionSerializer(quiz_session)
            
            return Response({
                "session": session_serializer.data,
                "questions": question_serializer.data,
                "total_questions": len(questions)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error starting quiz: {str(e)}")
            return Response(
                {"error": "Failed to start quiz", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuizSessionView(APIView):
    """Manage quiz sessions"""
    
    def get(self, request, session_id=None):
        """Get quiz session details"""
        if session_id:
            try:
                quiz_session = QuizSession.objects.get(session_id=session_id)
                serializer = QuizSessionSerializer(quiz_session)
                
                # Include answers if session is completed
                if quiz_session.is_completed:
                    answers = UserAnswer.objects.filter(quiz_session=quiz_session)
                    answer_serializer = UserAnswerSerializer(answers, many=True)
                    data = serializer.data
                    data['answers'] = answer_serializer.data
                    return Response(data)
                
                return Response(serializer.data)
                
            except QuizSession.DoesNotExist:
                return Response(
                    {"error": "Quiz session not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Return user's recent sessions
            sessions = QuizSession.objects.all().order_by('-started_at')[:20]
            if request.user.is_authenticated:
                sessions = sessions.filter(user=request.user)
            
            serializer = QuizSessionSerializer(sessions, many=True)
            return Response(serializer.data)

class SubmitAnswerView(APIView):
    """Submit an answer for a question"""
    
    def post(self, request):
        serializer = SubmitAnswerSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        session_id = serializer.validated_data['session_id']
        question_id = serializer.validated_data['question_id']
        user_answer = serializer.validated_data['answer']
        time_taken = serializer.validated_data.get('time_taken', 0.0)
        
        try:
            quiz_session = QuizSession.objects.get(session_id=session_id)
            question = QuizQuestion.objects.get(id=question_id)
            
            # Check if already answered
            existing_answer = UserAnswer.objects.filter(
                quiz_session=quiz_session,
                question=question
            ).first()
            
            if existing_answer:
                return Response(
                    {"error": "Question already answered"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if answer is correct
            is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
            
            # Save answer
            user_answer_obj = UserAnswer.objects.create(
                quiz_session=quiz_session,
                question=question,
                user_answer=user_answer,
                is_correct=is_correct,
                time_taken=time_taken
            )
            
            # Update session stats
            quiz_session.total_questions += 1
            if is_correct:
                quiz_session.correct_answers += 1
            
            quiz_session.score_percentage = (
                quiz_session.correct_answers / quiz_session.total_questions * 100
            )
            quiz_session.save()
            
            return Response({
                "is_correct": is_correct,
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
                "score": {
                    "correct_answers": quiz_session.correct_answers,
                    "total_questions": quiz_session.total_questions,
                    "percentage": round(quiz_session.score_percentage, 1)
                }
            })
            
        except QuizSession.DoesNotExist:
            return Response(
                {"error": "Quiz session not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except QuizQuestion.DoesNotExist:
            return Response(
                {"error": "Question not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CompleteQuizView(APIView):
    """Complete a quiz session"""
    
    def post(self, request, session_id):
        try:
            quiz_session = QuizSession.objects.get(session_id=session_id)
            
            if quiz_session.is_completed:
                return Response(
                    {"error": "Quiz already completed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            quiz_session.is_completed = True
            quiz_session.completed_at = timezone.now()
            
            # Calculate time taken
            if quiz_session.started_at:
                quiz_session.time_taken = quiz_session.completed_at - quiz_session.started_at
            
            quiz_session.save()
            
            # Get final results
            answers = UserAnswer.objects.filter(quiz_session=quiz_session).order_by('answered_at')
            answer_serializer = UserAnswerSerializer(answers, many=True)
            session_serializer = QuizSessionSerializer(quiz_session)
            
            return Response({
                "session": session_serializer.data,
                "answers": answer_serializer.data,
                "total_time": quiz_session.time_taken.total_seconds() if quiz_session.time_taken else 0
            })
            
        except QuizSession.DoesNotExist:
            return Response(
                {"error": "Quiz session not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET'])
def get_available_topics(request):
    """Get available topics for quiz generation"""
    topics = []
    
    if rag_service:
        try:
            # Get topics from RAG service
            rag_topics = rag_service.get_available_topics()
            topics.extend(rag_topics)
        except Exception as e:
            logger.error(f"Error getting RAG topics: {e}")
    
    # Add categories as topics
    categories = QuizCategory.objects.filter(is_active=True).values_list('name', flat=True)
    topics.extend(list(categories))
    
    # Remove duplicates and return
    unique_topics = list(set(topics))
    
    return JsonResponse({"topics": unique_topics})

@api_view(['GET'])
def quiz_stats(request):
    """Get quiz statistics"""
    total_questions = QuizQuestion.objects.filter(is_active=True).count()
    total_sessions = QuizSession.objects.count()
    completed_sessions = QuizSession.objects.filter(is_completed=True).count()
    
    avg_score = 0
    avg_time = 0
    
    if completed_sessions > 0:
        stats = QuizSession.objects.filter(is_completed=True).aggregate(
            avg_score=Avg('score_percentage'),
            avg_time=Avg('time_taken')
        )
        avg_score = stats['avg_score'] or 0
        if stats['avg_time']:
            avg_time = stats['avg_time'].total_seconds() / 60  # Convert to minutes
    
    # Category stats
    category_stats = QuizCategory.objects.filter(is_active=True).annotate(
        question_count=Count('questions', filter=models.Q(questions__is_active=True)),
        session_count=Count('quizsession')
    ).values('name', 'question_count', 'session_count')
    
    return JsonResponse({
        "total_questions": total_questions,
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "average_score": round(avg_score, 2),
        "average_time_minutes": round(avg_time, 2),
        "categories": list(category_stats)
    })