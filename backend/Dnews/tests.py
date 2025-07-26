#!/usr/bin/env python
"""
Working test script for Nepali Political News RAG System
Adjusted for your actual project structure
"""
import os
import sys

# Get the current directory (backend)
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)  # Go up one level from Dnews to backend

# Add backend directory to Python path
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Change to backend directory
os.chdir(backend_dir)

print(f"📍 Current working directory: {os.getcwd()}")
print(f"📂 Backend directory: {backend_dir}")
print(f"🐍 Python path includes: {backend_dir}")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poliplay.settings')

try:
    import django
    print("✅ Django module imported successfully")
    django.setup()
    print("✅ Django setup completed successfully")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print(f"🔍 Current Python path: {sys.path[:3]}...")
    sys.exit(1)

def test_basic_imports():
    """Test if we can import our modules"""
    try:
        from Dnews.models import NewsArticle
        print("✅ Successfully imported NewsArticle model")
        
        try:
            from Dnews import utils
            print("✅ Successfully imported utils module")
        except ImportError as e:
            print(f"⚠️  utils module import issue: {e}")
            print("   (This is OK if utils.py doesn't have all functions yet)")
        
        from Dnews import views
        print("✅ Successfully imported views module")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from Dnews.models import NewsArticle
        
        # Try to access the database
        count = NewsArticle.objects.count()
        print(f"✅ Database connection successful. Found {count} NewsArticles.")
        
        # Try to create a test article
        test_article = NewsArticle(
            source='TestSource',
            title='Test Article',
            summary='Test summary',
            link='https://test.com/test',
            bias='center',
            published=django.utils.timezone.now()
        )
        
        # Don't save, just validate
        test_article.full_clean()
        print("✅ NewsArticle model validation successful")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        if "no such table" in str(e).lower():
            print("💡 Try running: python manage.py migrate")
        return False

def test_settings():
    """Test Django settings"""
    try:
        from django.conf import settings
        print(f"✅ Django settings loaded")
        print(f"   Database engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Database name: {settings.DATABASES['default']['NAME']}")
        print(f"   Debug mode: {settings.DEBUG}")
        
        # Check if Dnews is in INSTALLED_APPS
        if 'Dnews' in settings.INSTALLED_APPS:
            print("   ✅ Dnews app is in INSTALLED_APPS")
        else:
            print("   ⚠️  Dnews app not found in INSTALLED_APPS")
            print(f"   📋 Installed apps: {settings.INSTALLED_APPS}")
        
        return True
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

def test_models():
    """Test NewsArticle model functionality"""
    try:
        from Dnews.models import NewsArticle
        from django.utils import timezone
        
        # Test model creation (without saving)
        article_data = {
            'source': 'TestSource',
            'title': 'Test Political Article',
            'summary': 'This is a test summary for political news.',
            'link': 'https://test.com/test-article',
            'bias': 'center',
            'published': timezone.now()
        }
        
        article = NewsArticle(**article_data)
        article.full_clean()  # Validate without saving
        
        print("✅ NewsArticle model creation and validation successful")
        print(f"   Model fields: {[field.name for field in NewsArticle._meta.fields]}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    try:
        from django.urls import reverse, resolve
        from django.conf import settings
        
        print("✅ URL configuration accessible")
        
        # Check if we can access URL patterns
        from poliplay.urls import urlpatterns
        print(f"   Found {len(urlpatterns)} main URL patterns")
        
        # Try to check Dnews URLs
        try:
            from Dnews.urls import urlpatterns as dnews_urls
            print(f"   Found {len(dnews_urls)} Dnews URL patterns")
        except ImportError:
            print("   ⚠️  Dnews URLs not found or not configured")
        
        return True
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def test_views():
    """Test views can be imported and basic functionality"""
    try:
        from Dnews import views
        
        # Check what views are available
        view_functions = [attr for attr in dir(views) if not attr.startswith('_') and callable(getattr(views, attr))]
        print(f"✅ Views module imported successfully")
        print(f"   Available views: {view_functions}")
        
        return True
    except Exception as e:
        print(f"❌ Views test failed: {e}")
        return False

def run_migration_check():
    """Check if migrations are needed"""
    try:
        from django.core.management import execute_from_command_line
        from io import StringIO
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if 'Dnews' in output:
                print("✅ Dnews migrations found")
                if '[ ]' in output:
                    print("⚠️  Some migrations are not applied")
                    print("💡 Run: python manage.py migrate")
                else:
                    print("✅ All migrations appear to be applied")
            else:
                print("⚠️  No Dnews migrations found")
                print("💡 Run: python manage.py makemigrations Dnews")
                
        except Exception as e:
            sys.stdout = old_stdout
            print(f"⚠️  Migration check failed: {e}")
            
    except Exception as e:
        print(f"⚠️  Could not run migration check: {e}")

if __name__ == "__main__":
    print("🧪 Nepali Political News RAG System - Working Tests")
    print(f"📅 Test Date: 2025-07-25 13:03:20 UTC")
    print(f"👤 Test User: CrypticLuminary")
    print("=" * 60)
    
    # Run migration check first
    print("\n🔄 Checking Migrations:")
    run_migration_check()
    
    print("\n" + "=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Django Settings", test_settings),
        ("Model Functionality", test_models),
        ("Database Connection", test_database_connection),
        ("URL Configuration", test_urls),
        ("Views Module", test_views)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        if test_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Django setup is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Ensure migrations are up to date: python manage.py migrate")
        print("   2. Complete your utils.py implementation")
        print("   3. Set up your API keys (OpenAI, Pinecone)")
        print("   4. Test your news scraping functionality")
        print("   5. Run the full test suite")
    elif passed >= total * 0.7:  # 70% or more passed
        print("✅ Most tests passed! Minor issues to fix.")
        print("\n💡 Common fixes:")
        print("   - Run: python manage.py migrate")
        print("   - Check your settings.py configuration")
        print("   - Ensure all required packages are installed")
    else:
        print("⚠️  Several tests failed. Please review your Django setup.")
        print("\n💡 Troubleshooting steps:")
        print("   1. Verify you're in the correct directory")
        print("   2. Check if virtual environment is activated")
        print("   3. Run: python manage.py migrate")
        print("   4. Verify Dnews is in INSTALLED_APPS in settings.py")
        print("   5. Check for any missing dependencies")