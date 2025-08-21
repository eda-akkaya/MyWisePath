#!/usr/bin/env python3
"""
Demo kullanıcı oluşturma scripti
Demo bilgilerle test için kullanıcı oluşturur
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def create_demo_user():
    """Demo kullanıcı oluştur"""
    
    demo_users = [
        {
            "username": "demo",
            "email": "demo@mywisepath.com",
            "password": "demo123"
        },
        {
            "username": "test",
            "email": "test@mywisepath.com", 
            "password": "test123"
        },
        {
            "username": "admin",
            "email": "admin@mywisepath.com",
            "password": "admin123"
        }
    ]
    
    print("🎯 Demo Kullanıcıları Oluşturuluyor...")
    print("="*50)
    
    for user_data in demo_users:
        try:
            # Kullanıcı kaydı
            response = requests.post(
                f"{API_BASE_URL}/api/v1/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {user_data['username']} kullanıcısı oluşturuldu")
                print(f"   📧 Email: {user_data['email']}")
                print(f"   🔑 Şifre: {user_data['password']}")
                print(f"   🆔 ID: {result.get('id', 'N/A')}")
                print()
                
                # Giriş testi
                login_response = requests.post(
                    f"{API_BASE_URL}/api/v1/auth/login",
                    json={
                        "email": user_data['email'],
                        "password": user_data['password']
                    }
                )
                
                if login_response.status_code == 200:
                    login_result = login_response.json()
                    print(f"✅ {user_data['username']} giriş testi başarılı")
                    print(f"   🎟️ Token: {login_result.get('token', 'N/A')[:50]}...")
                    print()
                else:
                    print(f"❌ {user_data['username']} giriş testi başarısız")
                    print(f"   Hata: {login_response.text}")
                    print()
                    
            else:
                error_detail = "Bilinmeyen hata"
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', error_detail)
                except:
                    error_detail = response.text
                    
                if "already registered" in error_detail.lower() or "already exists" in error_detail.lower():
                    print(f"ℹ️  {user_data['username']} kullanıcısı zaten mevcut")
                    print(f"   📧 Email: {user_data['email']}")
                    print(f"   🔑 Şifre: {user_data['password']}")
                    
                    # Mevcut kullanıcı için giriş testi
                    login_response = requests.post(
                        f"{API_BASE_URL}/api/v1/auth/login",
                        json={
                            "email": user_data['email'],
                            "password": user_data['password']
                        }
                    )
                    
                    if login_response.status_code == 200:
                        print(f"✅ Mevcut {user_data['username']} kullanıcısı ile giriş başarılı")
                    else:
                        print(f"❌ Mevcut {user_data['username']} kullanıcısı ile giriş başarısız")
                        print(f"   Hata: {login_response.text}")
                    print()
                else:
                    print(f"❌ {user_data['username']} kullanıcısı oluşturulamadı")
                    print(f"   Hata: {error_detail}")
                    print()
                    
        except requests.exceptions.ConnectionError:
            print("❌ Backend sunucusuna bağlanılamadı!")
            print("   Backend'in çalıştığından emin olun: python main.py")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {str(e)}")
            break
    
    print("="*50)
    print("🎉 Demo kullanıcı oluşturma işlemi tamamlandı!")
    print()
    print("📋 Giriş Bilgileri:")
    print("   demo@mywisepath.com / demo123")
    print("   test@mywisepath.com / test123") 
    print("   admin@mywisepath.com / admin123")
    print()
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend: http://localhost:8000")

if __name__ == "__main__":
    create_demo_user()
