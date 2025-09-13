#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_rebate.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_oauth():
    # 기본 사이트 설정
    site, created = Site.objects.get_or_create(
        domain='localhost:8000',
        defaults={'name': 'Crypto Rebate Local'}
    )
    
    if created:
        print(f"✅ Created site: {site.name}")
    else:
        print(f"✅ Using existing site: {site.name}")
    
    # Google Social Application 설정
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth',
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
        }
    )
    
    if created:
        print(f"✅ Created Google Social Application")
    else:
        print(f"✅ Using existing Google Social Application")
    
    # 사이트에 앱 연결
    google_app.sites.add(site)
    google_app.save()
    
    print(f"✅ Google OAuth setup completed!")
    print(f"   - Site: {site.domain}")
    print(f"   - Client ID: {google_app.client_id}")
    print(f"   - Sites: {list(google_app.sites.values_list('domain', flat=True))}")

if __name__ == '__main__':
    setup_google_oauth()
