from chatbot.services import rag_service
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from django.conf import settings
import json
import re
import logging
import os
from .models import QuizQuestion, QuizCategory

logger = logging.getLogger(__name__)

class QuizGenerationService:
    def __init__(self):
        openai_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
        
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            openai_api_key=openai_key
        )
        
        self.quiz_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert quiz question generator. Based on the provided context, 
            generate a multiple-choice question with exactly 5 options.
            
            Return the response in the following JSON format:
            {
                "question": "Your question here",
                "correct_answer": "The correct answer",
                "options": ["option1", "option2", "option3", "option4", "option5"],
                "difficulty": "easy|medium|hard",
                "explanation": "Brief explanation of why this is the correct answer"
            }
            
            Rules:
            - Make sure the correct answer is one of the 5 options
            - Make distractors plausible but clearly wrong
            - Keep questions clear and unambiguous
            - Focus on key concepts from the context
            - Vary difficulty levels appropriately
            
            Context: {context}"""),
            ("human", "Generate a {difficulty} difficulty quiz question about: {topic}")
        ])
    
    def generate_question_from_rag(self, topic, difficulty="medium", category_name="General"):
        """Generate a quiz question using RAG service"""
        try:
            if not rag_service:
                return None
            
            # Get relevant context from RAG
            similar_docs = rag_service.get_similar_documents(topic, k=3)
            
            if not similar_docs:
                return None
            
            # Combine context from similar documents
            context = "\n\n".join([doc['content'] for doc in similar_docs])
            
            # Generate question using LLM
            response = self.llm.invoke(
                self.quiz_prompt.format_messages(
                    context=context,
                    topic=topic,
                    difficulty=difficulty
                )
            )
            
            # Parse the response
            question_data = self._parse_llm_response(response.content)
            
            if question_data:
                # Get or create category
                category, _ = QuizCategory.objects.get_or_create(
                    name=category_name,
                    defaults={'description': f'Questions about {category_name}'}
                )
                
                # Save to database
                quiz_question = QuizQuestion.objects.create(
                    category=category,
                    question_text=question_data['question'],
                    correct_answer=question_data['correct_answer'],
                    options=question_data['options'],
                    difficulty=question_data.get('difficulty', difficulty),
                    explanation=question_data.get('explanation', ''),
                )
                
                return quiz_question
            
        except Exception as e:
            logger.error(f"Error generating question: {str(e)}")
            return None
    
    def _parse_llm_response(self, response_text):
        """Parse LLM response to extract question data"""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                question_data = json.loads(json_match.group())
                
                # Validate required fields
                required_fields = ['question', 'correct_answer', 'options']
                if all(field in question_data for field in required_fields):
                    # Ensure correct answer is in options
                    if question_data['correct_answer'] not in question_data['options']:
                        # Replace first option with correct answer
                        question_data['options'][0] = question_data['correct_answer']
                    
                    return question_data
            
            return None
            
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from LLM response")
            return None
    
    def generate_multiple_questions(self, topics, count=5, difficulty="medium", category_name="General"):
        """Generate multiple questions for given topics"""
        questions = []
        
        for i in range(count):
            topic = topics[i % len(topics)] if isinstance(topics, list) else topics
            question = self.generate_question_from_rag(topic, difficulty, category_name)
            if question:
                questions.append(question)
        
        return questions

# Global instance
quiz_generation_service = QuizGenerationService()