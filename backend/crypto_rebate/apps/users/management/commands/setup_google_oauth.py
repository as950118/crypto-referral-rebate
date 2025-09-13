from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Setup Google OAuth configuration'

    def handle(self, *args, **options):
        # 기본 사이트 설정
        site, created = Site.objects.get_or_create(
            domain='localhost:8000',
            defaults={'name': 'Crypto Rebate Local'}
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created site: {site.name}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Using existing site: {site.name}')
            )
        
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
            self.stdout.write(
                self.style.SUCCESS('✅ Created Google Social Application')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ Using existing Google Social Application')
            )
        
        # 사이트에 앱 연결
        google_app.sites.add(site)
        google_app.save()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Google OAuth setup completed!')
        )
        self.stdout.write(f'   - Site: {site.domain}')
        self.stdout.write(f'   - Client ID: {google_app.client_id}')
        self.stdout.write(f'   - Sites: {list(google_app.sites.values_list("domain", flat=True))}')
