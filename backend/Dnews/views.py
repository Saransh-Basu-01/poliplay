from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import embed_pending_articles, search_similar_articles, fetch_and_save_political_news
from .models import NewsArticle
import json

@api_view(['POST'])
def embed_news_articles(request):
    """API endpoint to embed pending articles"""
    try:
        result = embed_pending_articles()
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"Failed to embed articles: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def search_political_news(request):
    """Search for similar political news articles"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '')
        top_k = data.get('top_k', 5)
        
        if not query:
            return Response(
                {"error": "Query is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = search_similar_articles(query, top_k)
        
        # Format results
        formatted_results = []
        for match in results:
            formatted_results.append({
                "score": match.score,
                "title": match.metadata.get("title"),
                "summary": match.metadata.get("summary"),
                "source": match.metadata.get("source"),
                "link": match.metadata.get("link"),
                "bias": match.metadata.get("bias"),
                "published": match.metadata.get("published")
            })
        
        return Response({
            "success": True,
            "results": formatted_results,
            "total": len(formatted_results)
        })
        
    except Exception as e:
        return Response(
            {"error": f"Search failed: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def full_news_pipeline(request):
    """Complete pipeline: Fetch -> Save -> Embed news articles"""
    try:
        # Step 1: Fetch and save news
        fetch_result = fetch_and_save_political_news(request)
        if fetch_result.status_code != 200:
            return fetch_result
        
        # Step 2: Embed pending articles
        embed_result = embed_pending_articles()
        
        return Response({
            "success": True,
            "message": "Complete news pipeline executed successfully",
            "fetch_result": json.loads(fetch_result.content),
            "embed_result": embed_result
        })
        
    except Exception as e:
        return Response(
            {"error": f"Pipeline failed: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def news_stats(request):
    """Get statistics about news articles"""
    try:
        total_articles = NewsArticle.objects.count()
        embedded_articles = NewsArticle.objects.filter(embedded=True).count()
        pending_articles = NewsArticle.objects.filter(embedded=False).count()
        
        # Get stats by source
        source_stats = {}
        for article in NewsArticle.objects.all():
            source = article.source
            if source not in source_stats:
                source_stats[source] = {"total": 0, "embedded": 0}
            source_stats[source]["total"] += 1
            if article.embedded:
                source_stats[source]["embedded"] += 1
        
        return Response({
            "total_articles": total_articles,
            "embedded_articles": embedded_articles,
            "pending_articles": pending_articles,
            "embedding_rate": f"{(embedded_articles/total_articles*100):.1f}%" if total_articles > 0 else "0%",
            "source_breakdown": source_stats
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to get stats: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )