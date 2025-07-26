import feedparser
import openai
import pinecone
import hashlib
from django.conf import settings
from .models import NewsArticle
from django.utils import timezone
from dateutil import parser as date_parser
import logging

logger = logging.getLogger(__name__)

# News sources configuration
NEWS_SOURCES = {
    "OnlineKhabar": {
        "rss": "https://english.onlinekhabar.com/feed",
        "bias": "center-right"
    },
    "Republica": {
        "rss": "https://myrepublica.nagariknetwork.com/feed/",
        "bias": "center-left"
    },
    "KathmanduPost": {
        "rss": "https://kathmandupost.com/rss",
        "bias": "center"
    },
    "EkantiPur": {
        "rss": "https://ekantipur.com/feed",
        "bias": "center"
    }
}

def scrape_news(rss_url, source_name):
    """
    Scrape news from RSS feed and filter political content
    """
    try:
        feed = feedparser.parse(rss_url)
        articles = []
        
        for entry in feed.entries:
            # Check if the article is political (simple keyword check)
            title = entry.title.lower()
            if any(keyword in title for keyword in ['politic', 'government', 'parliament', 'election', 'minister', 'constitution', 'democracy']):
                article = {
                    'title': entry.title,
                    'summary': getattr(entry, 'summary', ''),
                    'link': entry.link,
                    'published': entry.published
                }
                articles.append(article)
        
        logger.info(f"Scraped {len(articles)} political articles from {source_name}")
        return articles
        
    except Exception as e:
        logger.error(f"Error scraping news from {source_name}: {e}")
        return []

def fetch_and_save_political_news():
    """
    Fetch political news from all sources and save to database
    """
    saved_count = 0
    duplicate_count = 0
    
    try:
        for source_name, source_info in NEWS_SOURCES.items():
            articles = scrape_news(source_info['rss'], source_name)
            
            for article_data in articles:
                try:
                    # Parse published date
                    published_date = date_parser.parse(article_data['published'])
                    
                    # Check if article already exists
                    if not NewsArticle.objects.filter(link=article_data['link']).exists():
                        NewsArticle.objects.create(
                            source=source_name,
                            title=article_data['title'],
                            summary=article_data['summary'],
                            link=article_data['link'],
                            bias=source_info['bias'],
                            published=published_date
                        )
                        saved_count += 1
                        logger.info(f"Saved article: {article_data['title'][:50]}...")
                    else:
                        duplicate_count += 1
                        logger.debug(f"Duplicate article skipped: {article_data['title'][:50]}...")
                        
                except Exception as e:
                    logger.error(f"Error saving article {article_data.get('title', 'Unknown')}: {e}")
        
        result = {
            "success": True,
            "saved": saved_count,
            "duplicates": duplicate_count,
            "total_processed": saved_count + duplicate_count
        }
        
        logger.info(f"News fetch completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in fetch_and_save_political_news: {e}")
        return {
            "success": False,
            "error": str(e),
            "saved": saved_count,
            "duplicates": duplicate_count
        }

# Initialize Pinecone
def initialize_pinecone():
    """Initialize Pinecone connection"""
    try:
        pinecone.init(
            api_key=getattr(settings, 'PINECONE_API_KEY', None),
            environment=getattr(settings, 'PINECONE_ENVIRONMENT', 'us-west1-gcp')
        )
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Pinecone: {e}")
        return False

def get_or_create_pinecone_index(index_name="nepali-political-news"):
    """Get existing index or create new one"""
    try:
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=1536,  # OpenAI embedding dimension
                metric="cosine"
            )
            logger.info(f"Created new Pinecone index: {index_name}")
        
        return pinecone.Index(index_name)
    except Exception as e:
        logger.error(f"Error with Pinecone index: {e}")
        return None

def generate_embedding(text, model="text-embedding-ada-002"):
    """Generate embedding using OpenAI"""
    try:
        openai.api_key = getattr(settings, 'OPENAI_API_KEY', None)
        response = openai.Embedding.create(
            model=model,
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None

def create_document_id(article):
    """Create unique document ID for Pinecone"""
    # Use article link and title to create unique ID
    unique_string = f"{article.link}_{article.title}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def embed_article_to_pinecone(article):
    """Embed single article to Pinecone"""
    try:
        # Initialize Pinecone
        if not initialize_pinecone():
            return False
        
        index = get_or_create_pinecone_index()
        if not index:
            return False
        
        # Prepare text for embedding (title + summary)
        embedding_text = f"{article.title}. {article.summary}"
        
        # Generate embedding
        embedding = generate_embedding(embedding_text)
        if not embedding:
            return False
        
        # Prepare metadata
        metadata = {
            "source": article.source,
            "title": article.title,
            "summary": article.summary[:500],  # Truncate for metadata limits
            "link": article.link,
            "bias": article.bias,
            "published": article.published.isoformat(),
            "content_type": "news_article",
            "language": "nepali_english"
        }
        
        # Create unique document ID
        doc_id = create_document_id(article)
        
        # Upsert to Pinecone
        index.upsert(vectors=[(doc_id, embedding, metadata)])
        
        # Mark as embedded in database
        article.embedded = True
        article.save()
        
        logger.info(f"Successfully embedded article: {article.title[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"Error embedding article {article.id}: {e}")
        return False

def embed_pending_articles():
    """Embed all articles that haven't been embedded yet"""
    try:
        pending_articles = NewsArticle.objects.filter(embedded=False)
        
        if not pending_articles.exists():
            logger.info("No pending articles to embed")
            return {"success": True, "message": "No pending articles", "embedded": 0}
        
        embedded_count = 0
        failed_count = 0
        
        for article in pending_articles:
            if embed_article_to_pinecone(article):
                embedded_count += 1
            else:
                failed_count += 1
        
        result = {
            "success": True,
            "embedded": embedded_count,
            "failed": failed_count,
            "total_processed": len(pending_articles)
        }
        
        logger.info(f"Embedding complete: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in embed_pending_articles: {e}")
        return {
            "success": False,
            "error": str(e),
            "embedded": 0,
            "failed": 0
        }

def search_similar_articles(query, top_k=5):
    """Search for similar articles in Pinecone"""
    try:
        if not initialize_pinecone():
            return []
        
        index = get_or_create_pinecone_index()
        if not index:
            return []
        
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        if not query_embedding:
            return []
        
        # Search in Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={"content_type": "news_article"}
        )
        
        return results.matches
        
    except Exception as e:
        logger.error(f"Error searching articles: {e}")
        return []