import requests
import feedparser
from datetime import datetime, timedelta
import json
import re
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

def translate_nepali_keywords():
    """Return Nepali political keywords for better filtering"""
    return {
        'political_nepali': [
            'सरकार', 'मन्त्री', 'प्रधानमन्त्री', 'राष्ट्रपति', 'संसद', 'मन्त्रिपरिषद',
            'नीति', 'निर्णय', 'कानून', 'ऐन', 'नियुक्ति', 'राजीनामा', 'गठन',
            'विघटन', 'चुनाव', 'निर्वाचन', 'राजनीतिक', 'दल', 'पार्टी'
        ],
        'announcement_nepali': [
            'सूचना', 'घोषणा', 'निर्देशिका', 'आदेश', 'अध्यादेश', 'प्रकाशन',
            'समाचार', 'विज्ञप्ति', 'अधिसूचना', 'निवेदन'
        ]
    }

def extract_content_from_page(url, timeout=15):
    """Extract actual content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5,ne;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.encoding = 'utf-8'  # Ensure proper encoding for Nepali text
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unnecessary elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find main content areas
            content_selectors = [
                '.content', '.main-content', '.post-content', '.article-content',
                '.news-content', '.description', '.detail', '.body',
                '#content', '#main-content', '#post-content',
                'article', '.article', '.post', '.news-item'
            ]
            
            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text(strip=True, separator=' ')
                    if len(content_text) > 100:  # Found substantial content
                        break
            
            # If no content found with selectors, try to get main text
            if not content_text or len(content_text) < 100:
                # Remove common navigation and sidebar elements
                for elem in soup.find_all(['nav', 'aside', 'header', 'footer']):
                    elem.decompose()
                
                # Get text from body or main content divs
                main_content = soup.find('body') or soup.find('div')
                if main_content:
                    content_text = main_content.get_text(strip=True, separator=' ')
            
            return content_text[:2000] if content_text else ""  # Limit content length
            
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return ""

def scrape_nepal_gov_portal():
    """Scrape nepal.gov.np for latest news and announcements"""
    base_url = "https://nepal.gov.np"
    articles = []
    
    try:
        print("Fetching from Nepal Government Portal...")
        
        # Try different sections of the website
        sections = [
            "/",
            "/news",
            "/notices", 
            "/press-releases",
            "/announcements"
        ]
        
        for section in sections:
            try:
                url = base_url + section
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for news/announcement elements
                    selectors = [
                        'a[href*="news"]', 'a[href*="notice"]', 'a[href*="press"]',
                        '.news-item', '.notice-item', '.announcement',
                        'h3 a', 'h4 a', '.title a', '.headline a'
                    ]
                    
                    found_links = set()
                    for selector in selectors:
                        elements = soup.select(selector)
                        
                        for element in elements[:5]:  # Limit per selector
                            title = element.get_text(strip=True)
                            link = element.get('href', '')
                            
                            if link and not link.startswith('http'):
                                link = urljoin(base_url, link)
                            
                            if title and link and len(title) > 10 and link not in found_links:
                                found_links.add(link)
                                
                                # Extract actual content from the linked page
                                content = extract_content_from_page(link)
                                
                                article = {
                                    'title': title,
                                    'text': content,
                                    'url': link,
                                    'publish_date': datetime.now().isoformat(),
                                    'source': 'Nepal Government Portal',
                                    'category': 'government_announcement',
                                    'language': 'nepali' if any(ord(char) > 127 for char in title) else 'english'
                                }
                                articles.append(article)
                                time.sleep(1)  # Delay between content extractions
                
            except Exception as e:
                print(f"Error with section {section}: {e}")
                continue
    
    except Exception as e:
        print(f"Error scraping Nepal Government Portal: {e}")
    
    print(f"  Found {len(articles)} articles from Nepal Government Portal")
    return articles

def scrape_opmcm_detailed():
    """Scrape Office of PM and Council of Ministers with detailed content"""
    base_url = "https://opmcm.gov.np"
    articles = []
    
    try:
        print("Fetching detailed content from PM Office...")
        
        # Try to find news/press releases section
        main_page = requests.get(base_url, timeout=15)
        main_page.encoding = 'utf-8'
        
        if main_page.status_code == 200:
            soup = BeautifulSoup(main_page.content, 'html.parser')
            
            # Look for news, press releases, or announcement links
            potential_links = soup.find_all('a', href=True)
            
            news_links = []
            for link in potential_links:
                href = link.get('href', '')
                text = link.get_text(strip=True).lower()
                
                # Look for news-related sections
                if any(keyword in text for keyword in ['समाचार', 'सूचना', 'विज्ञप्ति', 'news', 'press', 'notice']):
                    if not href.startswith('http'):
                        href = urljoin(base_url, href)
                    news_links.append((text, href))
            
            # Extract content from found news links
            for title, url in news_links[:10]:  # Limit to 10 links
                try:
                    content = extract_content_from_page(url)
                    if content and len(content) > 50:
                        article = {
                            'title': title,
                            'text': content,
                            'url': url,
                            'publish_date': datetime.now().isoformat(),
                            'source': 'Office of PM and Council of Ministers',
                            'category': 'government_announcement',
                            'language': 'nepali' if any(ord(char) > 127 for char in title) else 'english'
                        }
                        articles.append(article)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error extracting from {url}: {e}")
                    continue
    
    except Exception as e:
        print(f"Error scraping PM Office: {e}")
    
    print(f"  Found {len(articles)} detailed articles from PM Office")
    return articles

def scrape_parliament_detailed():
    """Scrape Parliament website for detailed content"""
    base_url = "https://hr.parliament.gov.np"
    articles = []
    
    try:
        print("Fetching detailed content from Parliament...")
        
        # Parliament might have different structure, try multiple approaches
        sections = [
            "/",
            "/news",
            "/notices",
            "/business",
            "/sessions"
        ]
        
        for section in sections:
            try:
                url = base_url + section
                response = requests.get(url, timeout=15)
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find links to detailed pages
                    links = soup.find_all('a', href=True)
                    
                    for link in links[:5]:  # Limit per section
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        if len(title) > 10 and href:
                            if not href.startswith('http'):
                                href = urljoin(base_url, href)
                            
                            # Extract detailed content
                            content = extract_content_from_page(href)
                            
                            if content and len(content) > 100:
                                article = {
                                    'title': title,
                                    'text': content,
                                    'url': href,
                                    'publish_date': datetime.now().isoformat(),
                                    'source': 'House of Representatives',
                                    'category': 'parliamentary_business',
                                    'language': 'nepali' if any(ord(char) > 127 for char in title) else 'english'
                                }
                                articles.append(article)
                            time.sleep(1)
                
            except Exception as e:
                print(f"Error with parliament section {section}: {e}")
                continue
    
    except Exception as e:
        print(f"Error scraping Parliament: {e}")
    
    print(f"  Found {len(articles)} detailed articles from Parliament")
    return articles

def scrape_law_commission_detailed():
    """Scrape Law Commission for detailed legal notices"""
    base_url = "https://lawcommission.gov.np"
    articles = []
    
    try:
        print("Fetching detailed content from Law Commission...")
        
        response = requests.get(base_url, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all content links
            content_links = soup.find_all('a', href=True)
            
            for link in content_links[:15]: 
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                # Skip external links and navigation
                if href.startswith('http') and 'lawcommission.gov.np' not in href:
                    continue
                
                if not href.startswith('http'):
                    href = urljoin(base_url, href)
                
                if len(title) > 10:
                    # Extract detailed content
                    content = extract_content_from_page(href)
                    
                    if content and len(content) > 100:
                        # Check if it's legal/government related
                        keywords = translate_nepali_keywords()
                        is_relevant = any(keyword in content.lower() for keyword in 
                                        keywords['political_nepali'] + keywords['announcement_nepali'])
                        
                        if is_relevant or 'कानून' in content or 'law' in content.lower():
                            article = {
                                'title': title,
                                'text': content,
                                'url': href,
                                'publish_date': datetime.now().isoformat(),
                                'source': 'Law Commission',
                                'category': 'legal_notice',
                                'language': 'nepali' if any(ord(char) > 127 for char in title) else 'english'
                            }
                            articles.append(article)
                    time.sleep(1)
    
    except Exception as e:
        print(f"Error scraping Law Commission: {e}")
    
    print(f"  Found {len(articles)} detailed articles from Law Commission")
    return articles

def scrape_reliable_nepali_news():
    """Scrape reliable Nepali news sources with full content"""
    articles = []
    
    # Reliable Nepali news sources
    news_sources = [
        {
            'name': 'Kathmandu Post',
            'rss': 'https://kathmandupost.com/rss',
            'base_url': 'https://kathmandupost.com'
        },
        {
            'name': 'The Himalayan Times', 
            'rss': 'https://thehimalayantimes.com/rss',
            'base_url': 'https://thehimalayantimes.com'
        },
        {
            'name': 'Online Khabar',
            'rss': 'https://english.onlinekhabar.com/feed',
            'base_url': 'https://english.onlinekhabar.com'
        }
    ]
    
    keywords = translate_nepali_keywords()
    political_keywords = keywords['political_nepali'] + [
        'government', 'minister', 'parliament', 'election', 'political',
        'coalition', 'party', 'cabinet', 'prime minister', 'president'
    ]
    
    for source in news_sources:
        try:
            print(f"Fetching detailed content from {source['name']}...")
            feed = feedparser.parse(source['rss'])
            
            for entry in feed.entries[:10]:  # Limit per source
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                link = entry.get('link', '')
                
                # Check if political content
                is_political = any(keyword in title.lower() or keyword in summary.lower() 
                                 for keyword in political_keywords)
                
                if is_political and link:
                    # Extract full article content
                    full_content = extract_content_from_page(link)
                    
                    if full_content and len(full_content) > 200:
                        article = {
                            'title': title,
                            'text': full_content,
                            'url': link,
                            'publish_date': entry.get('published', ''),
                            'source': source['name'],
                            'category': 'political_news',
                            'language': 'nepali' if any(ord(char) > 127 for char in title) else 'english'
                        }
                        articles.append(article)
                    time.sleep(1)
        
        except Exception as e:
            print(f"Error with {source['name']}: {e}")
            continue
    
    return articles

def get_comprehensive_nepal_content():
    """Get comprehensive Nepal political content with full text"""
    all_articles = []
    
    print("=== Starting Comprehensive Nepal Content Extraction ===\n")
    
    # Government sources with detailed content extraction
    print("=== Government Sources ===")
    
    # Nepal Government Portal
    gov_articles = scrape_nepal_gov_portal()
    all_articles.extend(gov_articles)
    time.sleep(2)
    
    # PM Office detailed
    pm_articles = scrape_opmcm_detailed()
    all_articles.extend(pm_articles)
    time.sleep(2)
    
    # Parliament detailed
    parliament_articles = scrape_parliament_detailed()
    all_articles.extend(parliament_articles)
    time.sleep(2)
    
    # Law Commission detailed
    law_articles = scrape_law_commission_detailed()
    all_articles.extend(law_articles)
    time.sleep(2)
    
    # News sources with full content
    print("\n=== News Sources ===")
    news_articles = scrape_reliable_nepali_news()
    all_articles.extend(news_articles)
    
    return all_articles

def save_enhanced_content(articles, filename="enhanced_nepal_political_content.json"):
    """Save enhanced content with full text and metadata"""
    
    # Filter and enhance articles
    enhanced_articles = []
    seen_urls = set()
    
    for article in articles:
        url = article.get('url', '')
        text = article.get('text', '')
        
        # Skip if no substantial content or duplicate
        if len(text) < 100 or url in seen_urls:
            continue
        
        seen_urls.add(url)
        
        # Add content analysis
        article['content_analysis'] = {
            'character_count': len(text),
            'word_count': len(text.split()),
            'has_nepali_content': any(ord(char) > 127 for char in text),
            'content_quality': 'high' if len(text) > 500 else 'medium' if len(text) > 200 else 'low'
        }
        
        enhanced_articles.append(article)
    
    # Categorize by content type and language
    categorized_data = {
        'government_announcements': [a for a in enhanced_articles if a.get('category') == 'government_announcement'],
        'parliamentary_business': [a for a in enhanced_articles if a.get('category') == 'parliamentary_business'],
        'legal_notices': [a for a in enhanced_articles if a.get('category') == 'legal_notice'],
        'political_news': [a for a in enhanced_articles if a.get('category') == 'political_news'],
        'nepali_content': [a for a in enhanced_articles if a.get('language') == 'nepali'],
        'english_content': [a for a in enhanced_articles if a.get('language') == 'english']
    }
    
    final_data = {
        'metadata': {
            'extraction_date': datetime.now().isoformat(),
            'total_articles': len(enhanced_articles),
            'sources': list(set([a.get('source', '') for a in enhanced_articles])),
            'categories': {k: len(v) for k, v in categorized_data.items()},
            'content_stats': {
                'avg_word_count': sum(a['content_analysis']['word_count'] for a in enhanced_articles) / len(enhanced_articles) if enhanced_articles else 0,
                'high_quality_articles': len([a for a in enhanced_articles if a['content_analysis']['content_quality'] == 'high']),
                'nepali_articles': len([a for a in enhanced_articles if a['content_analysis']['has_nepali_content']]),
            }
        },
        'articles': enhanced_articles
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(enhanced_articles)} enhanced articles to {filename}")
    print(f"Content Statistics:")
    print(f"  - High quality articles: {final_data['metadata']['content_stats']['high_quality_articles']}")
    print(f"  - Nepali content articles: {final_data['metadata']['content_stats']['nepali_articles']}")
    print(f"  - Average word count: {final_data['metadata']['content_stats']['avg_word_count']:.0f}")
    
    return filename

if __name__ == "__main__":
    print("=== Enhanced Nepal Political Content Extractor ===")
    print(f"Extraction started at: {datetime.now().isoformat()}")
    print("This will extract FULL CONTENT from Nepal government and news websites")
    print("Including Nepali language content")
    print("="*70)
    
    # Get comprehensive content
    all_content = get_comprehensive_nepal_content()
    
    print(f"\n=== Content Extraction Summary ===")
    print(f"Total articles extracted: {len(all_content)}")
    
    if all_content:
        # Display sample of what we got
        print(f"\n=== SAMPLE EXTRACTED CONTENT ===")
        for i, article in enumerate(all_content[:3], 1):
            print(f"\n--- Article {i} ---")
            print(f"Source: {article.get('source', 'N/A')}")
            print(f"Language: {article.get('language', 'N/A')}")
            print(f"Title: {article.get('title', 'N/A')[:100]}...")
            print(f"Content Length: {len(article.get('text', ''))} characters")
            print(f"Content Preview: {article.get('text', '')[:200]}...")
            print(f"URL: {article.get('url', 'N/A')}")
        
        # Save enhanced content
        filename = save_enhanced_content(all_content)
        print(f"\n=== EXTRACTION COMPLETE ===")
        print(f"Enhanced data saved to: {filename}")
        print(f"Ready for RAG model training with full content!")
        
    else:
        print("No content extracted. Check website accessibility and network connection.")