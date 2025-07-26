"""
Generate test data for the Nepali Political News RAG system
"""
import random
from datetime import datetime, timedelta
from django.utils import timezone

class TestDataGenerator:
    """Generate realistic test data for testing"""
    
    POLITICAL_KEYWORDS = [
        "parliament", "election", "political", "government", "constitution",
        "democracy", "policy", "minister", "prime minister", "coalition",
        "opposition", "vote", "bill", "legislation", "reform"
    ]
    
    NEWS_SOURCES = [
        "OnlineKhabar", "Republica", "KathmanduPost", "MyRepublica", "EkantiPur"
    ]
    
    BIAS_TYPES = ["center-left", "center", "center-right", "left", "right"]
    
    def generate_political_title(self):
        """Generate a realistic political news title"""
        templates = [
            "Nepal {} faces major challenges in {}",
            "Political parties discuss {} reform in {}",
            "New {} policy announced by {} government",
            "Opposition criticizes {} decision on {}",
            "{} coalition agrees on {} legislation"
        ]
        
        subjects = ["Parliament", "Government", "Opposition", "Coalition"]
        topics = ["constitutional", "economic", "social", "electoral", "judicial"]
        
        template = random.choice(templates)
        return template.format(
            random.choice(subjects), 
            random.choice(topics)
        )
    
    def generate_political_summary(self, title):
        """Generate a summary based on the title"""
        summaries = [
            f"In a significant development, {title.lower()}. This decision is expected to have major implications for Nepal's political landscape.",
            f"Recent discussions regarding {title.lower()} have sparked debate among political analysts and citizens alike.",
            f"The announcement of {title.lower()} marks a crucial moment in Nepal's democratic process and governance."
        ]
        return random.choice(summaries)
    
    def generate_test_articles(self, count=10):
        """Generate a list of test articles"""
        articles = []
        base_date = timezone.now()
        
        for i in range(count):
            title = self.generate_political_title()
            article = {
                'source': random.choice(self.NEWS_SOURCES),
                'title': title,
                'summary': self.generate_political_summary(title),
                'link': f"https://test{i}.com/article-{i}",
                'bias': random.choice(self.BIAS_TYPES),
                'published': base_date - timedelta(hours=i)
            }
            articles.append(article)
        
        return articles
    
    def generate_rss_feed_mock(self, count=5):
        """Generate mock RSS feed data"""
        articles = self.generate_test_articles(count)
        
        mock_entries = []
        for article in articles:
            entry = type('MockEntry', (), {
                'title': article['title'],
                'summary': article['summary'],
                'link': article['link'],
                'published': article['published'].strftime('%a, %d %b %Y %H:%M:%S GMT')
            })()
            mock_entries.append(entry)
        
        return type('MockFeed', (), {'entries': mock_entries})()

# Usage in tests:
# generator = TestDataGenerator()
# test_articles = generator.generate_test_articles(20)
# mock_feed = generator.generate_rss_feed_mock(10)