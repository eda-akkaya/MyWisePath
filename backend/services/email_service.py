import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import os
from datetime import datetime, timedelta
import json
from config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
    EMAIL_FROM, EMAIL_FROM_NAME
)

class EmailService:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.smtp_username = SMTP_USERNAME
        self.smtp_password = SMTP_PASSWORD
        self.email_from = EMAIL_FROM
        self.email_from_name = EMAIL_FROM_NAME
        
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """
        E-posta gönder
        """
        try:
            # Test modu - gerçek e-posta göndermek yerine log yazdır
            if not self.smtp_username or not self.smtp_password:
                print(f"📧 TEST MODU - E-posta gönderilecek:")
                print(f"   To: {to_email}")
                print(f"   Subject: {subject}")
                print(f"   From: {self.email_from_name} <{self.email_from}>")
                print(f"   HTML Content Length: {len(html_content)} characters")
                if text_content:
                    print(f"   Text Content Length: {len(text_content)} characters")
                print(f"✅ Test e-postası başarıyla simüle edildi: {to_email}")
                return True
            
            # E-posta mesajını oluştur
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.email_from_name} <{self.email_from}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # HTML içeriği ekle
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Text içeriği varsa ekle
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)
            
            # SMTP bağlantısı kur ve gönder
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"E-posta başarıyla gönderildi: {to_email}")
            return True
            
        except Exception as e:
            print(f"E-posta gönderme hatası: {e}")
            print(f"SMTP Ayarları: Server={self.smtp_server}, Port={self.smtp_port}, Username={'Set' if self.smtp_username else 'Not Set'}")
            return False
    
    def send_weekly_reminder(self, user_email: str, username: str, learning_goals: List[str] = None) -> bool:
        """
        Haftalık öğrenme hatırlatıcısı gönder
        """
        subject = "🎯 MyWisePath - Bu Hafta Öğrenmeye Devam Edin!"
        
        # HTML içeriği
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Haftalık Hatırlatıcı</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2563eb;
                    margin-bottom: 10px;
                }}
                .greeting {{
                    font-size: 18px;
                    margin-bottom: 20px;
                }}
                .content {{
                    margin-bottom: 30px;
                }}
                .goals {{
                    background-color: #f8fafc;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .goal-item {{
                    margin: 10px 0;
                    padding: 10px;
                    background-color: white;
                    border-left: 4px solid #2563eb;
                    border-radius: 4px;
                }}
                .cta-button {{
                    display: inline-block;
                    background-color: #2563eb;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    color: #6b7280;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🎓 MyWisePath</div>
                    <h1>Haftalık Öğrenme Hatırlatıcısı</h1>
                </div>
                
                <div class="greeting">
                    Merhaba <strong>{username}</strong>! 👋
                </div>
                
                <div class="content">
                    <p>Bu hafta öğrenme yolculuğunuza devam etmek için harika bir zaman! 
                    Her gün biraz zaman ayırarak büyük ilerlemeler kaydedebilirsiniz.</p>
                    
                    <h3>💡 Bu Hafta İçin Öneriler:</h3>
                    <ul>
                        <li>Günde en az 30 dakika öğrenmeye ayırın</li>
                        <li>Pratik yapmak için küçük projeler geliştirin</li>
                        <li>Öğrendiklerinizi not alın ve tekrar edin</li>
                        <li>Topluluk forumlarında sorular sorun</li>
                    </ul>
                </div>
                
                {f'''
                <div class="goals">
                    <h3>🎯 Öğrenme Hedefleriniz:</h3>
                    {''.join([f'<div class="goal-item">• {goal}</div>' for goal in (learning_goals or [])])}
                </div>
                ''' if learning_goals else ''}
                
                <div style="text-align: center;">
                    <a href="http://localhost:3000/dashboard" class="cta-button">
                        Öğrenmeye Devam Et →
                    </a>
                </div>
                
                <div class="footer">
                    <p>Bu e-postayı almak istemiyorsanız, <a href="#">abonelikten çıkın</a></p>
                    <p>© 2024 MyWisePath. Tüm hakları saklıdır.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Text içeriği
        text_content = f"""
        Merhaba {username}!

        Bu hafta öğrenme yolculuğunuza devam etmek için harika bir zaman! 
        Her gün biraz zaman ayırarak büyük ilerlemeler kaydedebilirsiniz.

        Bu Hafta İçin Öneriler:
        - Günde en az 30 dakika öğrenmeye ayırın
        - Pratik yapmak için küçük projeler geliştirin
        - Öğrendiklerinizi not alın ve tekrar edin
        - Topluluk forumlarında sorular sorun

        {f'Öğrenme Hedefleriniz: {", ".join(learning_goals or [])}' if learning_goals else ''}

        Öğrenmeye devam etmek için: http://localhost:3000/dashboard

        © 2024 MyWisePath
        """
        
        return self.send_email(user_email, subject, html_content, text_content)
    
    def send_progress_report(self, user_email: str, username: str, progress_data: dict) -> bool:
        """
        İlerleme raporu gönder
        """
        subject = "📊 MyWisePath - İlerleme Raporunuz Hazır!"
        
        # İlerleme verilerini hazırla
        completed_topics = progress_data.get('completed_topics', [])
        current_streak = progress_data.get('current_streak', 0)
        total_study_time = progress_data.get('total_study_time', 0)
        next_goals = progress_data.get('next_goals', [])
        
        # HTML içeriği
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>İlerleme Raporu</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2563eb;
                    margin-bottom: 10px;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }}
                .stat-card {{
                    background-color: #f8fafc;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .stat-number {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2563eb;
                }}
                .stat-label {{
                    font-size: 14px;
                    color: #6b7280;
                    margin-top: 5px;
                }}
                .completed-topics {{
                    background-color: #f0fdf4;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .next-goals {{
                    background-color: #fef3c7;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .cta-button {{
                    display: inline-block;
                    background-color: #2563eb;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    color: #6b7280;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">📊 MyWisePath</div>
                    <h1>İlerleme Raporunuz</h1>
                </div>
                
                <div class="greeting">
                    Merhaba <strong>{username}</strong>! 👋
                </div>
                
                <div class="content">
                    <p>Öğrenme yolculuğunuzda harika ilerlemeler kaydediyorsunuz! 
                    İşte son durumunuz:</p>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{len(completed_topics)}</div>
                        <div class="stat-label">Tamamlanan Konu</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{current_streak}</div>
                        <div class="stat-label">Günlük Seri</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{total_study_time}</div>
                        <div class="stat-label">Toplam Saat</div>
                    </div>
                </div>
                
                {f'''
                <div class="completed-topics">
                    <h3>✅ Tamamladığınız Konular:</h3>
                    {''.join([f'<div>• {topic}</div>' for topic in completed_topics])}
                </div>
                ''' if completed_topics else ''}
                
                {f'''
                <div class="next-goals">
                    <h3>🎯 Sıradaki Hedefleriniz:</h3>
                    {''.join([f'<div>• {goal}</div>' for goal in next_goals])}
                </div>
                ''' if next_goals else ''}
                
                <div style="text-align: center;">
                    <a href="http://localhost:3000/dashboard" class="cta-button">
                        Detaylı Raporu Görüntüle →
                    </a>
                </div>
                
                <div class="footer">
                    <p>Bu e-postayı almak istemiyorsanız, <a href="#">abonelikten çıkın</a></p>
                    <p>© 2024 MyWisePath. Tüm hakları saklıdır.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Text içeriği
        text_content = f"""
        Merhaba {username}!

        Öğrenme yolculuğunuzda harika ilerlemeler kaydediyorsunuz! 
        İşte son durumunuz:

        İstatistikler:
        - Tamamlanan Konu: {len(completed_topics)}
        - Günlük Seri: {current_streak} gün
        - Toplam Çalışma Süresi: {total_study_time} saat

        {f'Tamamladığınız Konular: {", ".join(completed_topics)}' if completed_topics else ''}
        {f'Sıradaki Hedefleriniz: {", ".join(next_goals)}' if next_goals else ''}

        Detaylı raporu görüntülemek için: http://localhost:3000/dashboard

        © 2024 MyWisePath
        """
        
        return self.send_email(user_email, subject, html_content, text_content)

# Global email service instance
email_service = EmailService() 