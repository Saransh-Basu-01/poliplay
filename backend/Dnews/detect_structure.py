#!/usr/bin/env python
"""
Detect Django project structure
"""
import os
import sys

def detect_django_structure():
    """Detect Django project structure and settings"""
    print("🔍 Django Project Structure Detection")
    print("=" * 40)
    
    current_dir = os.getcwd()
    print(f"📍 Current Directory: {current_dir}")
    
    # Check for manage.py
    if os.path.exists('manage.py'):
        print("✅ Found manage.py - This is a Django project root")
        
        # Read manage.py to find settings
        with open('manage.py', 'r') as f:
            content = f.read()
            print("\n📄 manage.py content preview:")
            lines = content.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            
            # Extract settings module
            import re
            match = re.search(r"'([^']+\.settings)'", content)
            if match:
                settings_module = match.group(1)
                print(f"\n✅ Found settings module: {settings_module}")
            else:
                print("\n❌ Could not find settings module in manage.py")
    else:
        print("❌ No manage.py found - Not in Django project root")
    
    # Look for settings.py files
    print("\n🔍 Looking for settings.py files:")
    settings_files = []
    
    for root, dirs, files in os.walk('.'):
        if 'settings.py' in files:
            settings_path = os.path.join(root, 'settings.py')
            settings_files.append(settings_path)
            print(f"   ✅ Found: {settings_path}")
    
    if not settings_files:
        print("   ❌ No settings.py files found")
    
    # Look for Django apps
    print("\n🔍 Looking for Django apps:")
    apps = []
    
    for item in os.listdir('.'):
        if os.path.isdir(item):
            app_py = os.path.join(item, 'apps.py')
            models_py = os.path.join(item, 'models.py')
            views_py = os.path.join(item, 'views.py')
            
            if os.path.exists(app_py) or (os.path.exists(models_py) and os.path.exists(views_py)):
                apps.append(item)
                print(f"   ✅ Found Django app: {item}")
                
                # Check app contents
                app_files = os.listdir(item)
                important_files = ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']
                for file in important_files:
                    if file in app_files:
                        print(f"      ✅ {file}")
                    else:
                        print(f"      ❌ {file}")
    
    if not apps:
        print("   ❌ No Django apps found")
    
    # Check for common Django files
    print("\n🔍 Checking for common Django files:")
    common_files = ['requirements.txt', 'db.sqlite3', '__pycache__']
    
    for file in common_files:
        if os.path.exists(file):
            print(f"   ✅ Found: {file}")
        else:
            print(f"   ❌ Missing: {file}")
    
    # Suggest correct settings module
    print("\n💡 Recommendations:")
    
    if settings_files:
        for settings_file in settings_files:
            # Convert path to module format
            module_path = settings_file.replace('\\', '/').replace('/', '.').replace('.py', '').lstrip('.')
            print(f"   Try: DJANGO_SETTINGS_MODULE='{module_path}'")
    
    if apps:
        print(f"   Found {len(apps)} Django app(s): {', '.join(apps)}")
    
    print("\n🔧 To fix your tests:")
    print("   1. Make sure you're in the Django project root (where manage.py is)")
    print("   2. Use the correct settings module path")
    print("   3. Ensure your app is in INSTALLED_APPS")

if __name__ == "__main__":
    detect_django_structure()