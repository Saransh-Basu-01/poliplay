#!/usr/bin/env python
"""
Run tests using Django management command approach
"""
import os
import sys

# Get current directory and adjust path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)

# Change to backend directory
os.chdir(backend_dir)

# Use Django's management utility
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poliplay.settings')
    try:
        from django.core.management import execute_from_command_line
        
        print("🧪 Running Django Tests for Dnews App")
        print("=" * 40)
        
        # Run Django's built-in test command
        execute_from_command_line(['manage.py', 'test', 'Dnews', '--verbosity=2'])
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc