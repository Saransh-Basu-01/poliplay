from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from django.conf import settings
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Get API keys from environment or settings
        openai_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
        pinecone_key = getattr(settings, 'PINECONE_API_KEY', None) or os.getenv('PINECONE_API_KEY')
        
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in settings or environment")
        
        if not pinecone_key:
            logger.warning("PINECONE_API_KEY not found - some features may not work")
            
        self.embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=openai_key
        )
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            openai_api_key=openai_key
        )
        self.index_name = "pine-chatbbot"
        self.vectorstore = None
        self.rag_chain = None
        
        # Document loading configuration
        self.data_directory = os.path.join(settings.BASE_DIR, 'chatbot', 'data')
        self.documents_loaded = False
        
        self._initialize_rag_chain()
    
    def _load_documents(self):
        """Load documents from the data directory"""
        try:
            # Check if data directory exists
            if not os.path.exists(self.data_directory):
                logger.warning(f"Data directory not found: {self.data_directory}")
                return []
            
            logger.info(f"Loading documents from: {self.data_directory}")
            
            # Load documents using DirectoryLoader (same as your Jupyter notebook)
            loader = DirectoryLoader(
                self.data_directory,
                glob="**/*",  # Load all files
                loader_cls=UnstructuredFileLoader,
                show_progress=True
            )
            
            raw_documents = loader.load()
            logger.info(f"Loaded {len(raw_documents)} raw documents")
            
            if not raw_documents:
                logger.warning("No documents found in data directory")
                return []
            
            # Split documents into chunks (same as your Jupyter notebook)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=100,
                length_function=len,
                is_separator_regex=False,
            )
            
            split_docs = text_splitter.split_documents(raw_documents)
            logger.info(f"Split into {len(split_docs)} document chunks")
            
            return split_docs
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            return []
    
    def _initialize_rag_chain(self):
        """Initialize the RAG chain with Pinecone vectorstore"""
        try:
            # First, try to connect to existing vectorstore
            try:
                self.vectorstore = PineconeVectorStore(
                    index_name=self.index_name,
                    embedding=self.embeddings_model
                )
                logger.info("Connected to existing Pinecone index")
                
            except Exception as e:
                logger.warning(f"Could not connect to existing index: {e}")
                # If no existing index, load documents and create new one
                split_docs = self._load_documents()
                
                if split_docs:
                    logger.info("Creating new Pinecone vectorstore with documents")
                    self.vectorstore = PineconeVectorStore.from_documents(
                        split_docs, 
                        self.embeddings_model, 
                        index_name=self.index_name
                    )
                    self.documents_loaded = True
                    logger.info(f"Created vectorstore with {len(split_docs)} document chunks")
                else:
                    logger.error("No documents to load and no existing vectorstore")
                    return
            
            # Updated system prompt to match your Jupyter notebook behavior
            system_prompt = (
                "You are a legal document assistant. "
                "Use the provided context from the documents when available. "
                "If the context contains relevant information, base your answer on it. "
                "If the context doesn't contain specific information to answer the question, "
                "you may provide general legal knowledge while noting that specific information "
                "is not available in the provided documents. "
                "Always respond in the same language as the question. "
                "Never mention that the information is not in the document"
                "Always present as if the data was present the document"
                "Answer the question in englis if the question is in english and answer in nepali if the question is in nepali do not divert"
                "Never refer to the source just give the answer as if you are the source"
                "\n\nContext from documents: {context}"
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])
            
            # Create chains
            question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
            self.rag_chain = create_retrieval_chain(
                self.vectorstore.as_retriever(), 
                question_answer_chain
            )
            
            logger.info("RAG chain initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG chain: {str(e)}")
            self.rag_chain = None
    
    def reload_documents(self):
        """Reload documents from data directory"""
        try:
            split_docs = self._load_documents()
            
            if split_docs:
                # Recreate vectorstore with new documents
                self.vectorstore = PineconeVectorStore.from_documents(
                    split_docs, 
                    self.embeddings_model, 
                    index_name=self.index_name
                )
                
                # Reinitialize RAG chain
                self._initialize_rag_chain()
                self.documents_loaded = True
                return f"Successfully reloaded {len(split_docs)} document chunks"
            else:
                return "No documents found to reload"
                
        except Exception as e:
            logger.error(f"Error reloading documents: {str(e)}")
            return f"Error reloading documents: {str(e)}"
    
    def get_document_status(self):
        """Get status of loaded documents"""
        return {
            "documents_loaded": self.documents_loaded,
            "data_directory": self.data_directory,
            "data_directory_exists": os.path.exists(self.data_directory),
            "vectorstore_available": self.vectorstore is not None,
            "rag_chain_available": self.rag_chain is not None
        }
    
    def ask_question(self, question: str) -> str:
        """Process a question through the RAG chain"""
        try:
            if not self.rag_chain:
                return "RAG system is not properly initialized. Please check your configuration and document loading."
            
            response = self.rag_chain.invoke({"input": question})
            return response["answer"]
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return f"Error processing your question: {str(e)}"
    
    def get_similar_documents(self, question: str, k: int = 4):
        """Get similar documents for a question"""
        try:
            if not self.vectorstore:
                return []
            
            similar_docs = self.vectorstore.similarity_search(question, k=k)
            return [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "id": getattr(doc, 'id', 'Unknown')
                }
                for doc in similar_docs
            ]
            
        except Exception as e:
            logger.error(f"Error getting similar documents: {str(e)}")
            return []

# Global instance - will be initialized when imported
try:
    rag_service = RAGService()
except Exception as e:
    logger.error(f"Failed to initialize RAG service: {e}")
    rag_service = None