import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time
import re
from tqdm import tqdm

# Enhanced government sites with specific document sections
GOV_SITES = {
    "Law Commission": {
        "base": "https://lawcommission.gov.np/",
        "sections": [
            "https://lawcommission.gov.np/category/acts/",
            "https://lawcommission.gov.np/category/reports/",
            "https://lawcommission.gov.np/category/publications/"
        ]
    },
    "Ministry of Health": {
        "base": "https://mohp.gov.np/",
        "sections": [
            "https://mohp.gov.np/downloads/",
            "https://mohp.gov.np/category/reports/",
            "https://mohp.gov.np/category/policies/"
        ]
    },
    "Ministry of Finance": {
        "base": "https://mof.gov.np/",
        "sections": [
            "https://mof.gov.np/site/publication-detail/1",
            "https://mof.gov.np/uploads/document/file/",
        ]
    },
    "Ministry of Home Affairs": {
        "base": "https://moha.gov.np/",
        "sections": [
            "https://moha.gov.np/category/reports/",
            "https://moha.gov.np/category/acts/"
        ]
    }
}

CURRENT_DIR = Path(__file__).resolve().parent
SAVE_DIR = os.path.join(CURRENT_DIR, "data")
os.makedirs(SAVE_DIR, exist_ok=True)

def get_session():
    """Create a requests session with proper headers"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    return session

def is_pdf_url(url):
    return url.lower().endswith(".pdf") or ".pdf" in url.lower()

def is_document_url(url):
    """Check if URL might lead to documents"""
    doc_indicators = [
        'document', 'download', 'file', 'report', 'publication', 
        'act', 'law', 'policy', 'notice', 'circular', 'guidelines'
    ]
    return any(indicator in url.lower() for indicator in doc_indicators)

def clean_filename(filename):
    """Clean filename for safe saving"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:90] + ext
    return filename

def download_pdf(pdf_url, save_dir, session, ministry_name=""):
    """Download PDF with proper error handling"""
    try:
        # Get filename from URL
        parsed_url = urlparse(pdf_url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or not filename.endswith('.pdf'):
            filename = f"document_{hash(pdf_url)}.pdf"
        
        # Add ministry prefix
        if ministry_name:
            filename = f"{ministry_name}_{filename}"
        
        filename = clean_filename(filename)
        filepath = os.path.join(save_dir, filename)

        # Skip if already exists
        if os.path.exists(filepath):
            print(f"⏭️  Already exists: {filename}")
            return True

        print(f"📥 Downloading: {pdf_url}")
        
        response = session.get(pdf_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Check if it's actually a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not pdf_url.lower().endswith('.pdf'):
            print(f"⚠️  Not a PDF: {pdf_url} (Content-Type: {content_type})")
            return False

        # Download the file
        total_size = int(response.headers.get('content-length', 0))
        with open(filepath, "wb") as f:
            if total_size > 0:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
        print(f"✅ Downloaded: {filename} ({os.path.getsize(filepath)} bytes)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error downloading {pdf_url}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error downloading {pdf_url}: {e}")
        return False

def find_pdfs_in_page(url, session, visited_urls=None, depth=0, max_depth=2):
    """Recursively find PDFs in a webpage"""
    if visited_urls is None:
        visited_urls = set()
    
    if url in visited_urls or depth > max_depth:
        return set()
    
    visited_urls.add(url)
    pdf_links = set()
    
    try:
        print(f"🔍 Scanning: {url} (depth: {depth})")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all links
        links = soup.find_all("a", href=True)
        
        for link in links:
            href = link.get('href', '').strip()
            if not href:
                continue
            
            # Make absolute URL
            full_url = urljoin(url, href)
            
            # Skip external links (different domain)
            if urlparse(full_url).netloc != urlparse(url).netloc:
                continue
            
            # If it's a PDF, add it
            if is_pdf_url(full_url):
                pdf_links.add(full_url)
                print(f"🎯 Found PDF: {full_url}")
            
            # If it looks like a document page and we haven't gone too deep, explore it
            elif depth < max_depth and is_document_url(full_url):
                sub_pdfs = find_pdfs_in_page(full_url, session, visited_urls, depth + 1, max_depth)
                pdf_links.update(sub_pdfs)
        
        # Also look for PDFs in text content (sometimes links are in JavaScript or other places)
        text_content = soup.get_text()
        pdf_patterns = re.findall(r'https?://[^\s]+\.pdf', text_content, re.IGNORECASE)
        for pdf_url in pdf_patterns:
            pdf_links.add(pdf_url)
            print(f"🎯 Found PDF in content: {pdf_url}")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error accessing {url}: {e}")
    except Exception as e:
        print(f"⚠️  Error parsing {url}: {e}")
    
    return pdf_links

def scrape_ministry_pdfs(ministry_name, ministry_config, session):
    """Scrape PDFs from a specific ministry"""
    print(f"\n🏛️  Scraping {ministry_name}")
    print("=" * 50)
    
    all_pdf_links = set()
    
    # Check base URL
    base_pdfs = find_pdfs_in_page(ministry_config["base"], session)
    all_pdf_links.update(base_pdfs)
    
    # Check specific sections
    for section_url in ministry_config.get("sections", []):
        try:
            section_pdfs = find_pdfs_in_page(section_url, session)
            all_pdf_links.update(section_pdfs)
            time.sleep(1)  # Be respectful
        except Exception as e:
            print(f"⚠️  Error with section {section_url}: {e}")
    
    print(f"📊 Total PDFs found for {ministry_name}: {len(all_pdf_links)}")
    
    # Download PDFs
    downloaded_count = 0
    ministry_short = ministry_name.replace(" ", "_").replace("Ministry_of_", "")
    
    for pdf_url in all_pdf_links:
        if download_pdf(pdf_url, SAVE_DIR, session, ministry_short):
            downloaded_count += 1
        time.sleep(0.5)  # Small delay between downloads
    
    print(f"✅ Downloaded {downloaded_count} PDFs from {ministry_name}")
    return downloaded_count

def scrape_and_download_all_pdfs():
    """Main function to scrape all PDFs"""
    print("🚀 Starting Enhanced PDF Scraping from Nepal Government Sites")
    print(f"📁 Save directory: {SAVE_DIR}")
    print("=" * 70)
    
    session = get_session()
    total_downloaded = 0
    
    for ministry_name, ministry_config in GOV_SITES.items():
        try:
            count = scrape_ministry_pdfs(ministry_name, ministry_config, session)
            total_downloaded += count
            time.sleep(2)  # Delay between ministries
        except Exception as e:
            print(f"❌ Error with {ministry_name}: {e}")
            continue
    
    print(f"\n🎉 SCRAPING COMPLETE!")
    print(f"📊 Total PDFs downloaded: {total_downloaded}")
    print(f"📁 Files saved in: {SAVE_DIR}")
    
    # List downloaded files
    if total_downloaded > 0:
        print(f"\n📋 Downloaded files:")
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith('.pdf'):
                filepath = os.path.join(SAVE_DIR, filename)
                size = os.path.getsize(filepath)
                print(f"  • {filename} ({size:,} bytes)")
    
    return total_downloaded

if __name__ == "__main__":
    # Run the scraper
    total = scrape_and_download_all_pdfs()
    
    if total == 0:
        print("\n🤔 No PDFs found. This might be because:")
        print("  • Websites have changed their structure")
        print("  • Anti-scraping measures are in place")
        print("  • Network connectivity issues")
        print("  • PDFs are behind authentication")
        print("\n💡 Try running with verbose output to see what's happening")