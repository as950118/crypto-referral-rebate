#!/usr/bin/env python
import os
import django
import requests

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_rebate.settings')
django.setup()

def test_google_auth():
    print("🔍 Testing Google Auth API...")
    
    # 테스트용 credential (실제로는 Google에서 받은 토큰이어야 함)
    test_credential = "test_credential"
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/google/',
            json={'credential': test_credential},
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 403:
            print("❌ 403 Forbidden - 권한 문제")
        elif response.status_code == 400:
            print("✅ API는 작동하지만 credential이 유효하지 않음 (정상)")
        else:
            print(f"Response: {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. Django 서버가 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == '__main__':
    test_google_auth()
