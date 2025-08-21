"""
PDF Generator - Roadmap'leri PDF formatında oluşturma ve indirme
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
from datetime import datetime

# PDF generation imports
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

class PDFGenerator:
    """PDF oluşturma ve indirme için ana sınıf"""
    
    def __init__(self, output_directory: str = "./pdfs"):
        """
        Args:
            output_directory: PDF dosyalarının kaydedileceği dizin
        """
        self.output_directory = output_directory
        self.styles = getSampleStyleSheet()
        
        # Özel stiller oluştur
        self._create_custom_styles()
        
        # Çıktı dizinini oluştur
        os.makedirs(output_directory, exist_ok=True)
        
        logger.info(f"PDF Generator başlatıldı: {output_directory}")
    
    def _create_custom_styles(self):
        """Özel PDF stilleri oluşturur"""
        # Başlık stili
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Alt başlık stili
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkgreen
        ))
        
        # Modül başlığı stili
        self.styles.add(ParagraphStyle(
            name='ModuleTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=15,
            textColor=colors.darkred,
            leftIndent=20
        ))
        
        # Normal metin stili
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))
        
        # Kaynak stili
        self.styles.add(ParagraphStyle(
            name='ResourceStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=30,
            textColor=colors.grey
        ))
    
    def generate_roadmap_pdf(self, 
                           roadmap_data: Dict[str, Any],
                           user_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Roadmap'i PDF formatında oluşturur
        
        Args:
            roadmap_data: Roadmap verisi
            user_info: Kullanıcı bilgileri (opsiyonel)
            
        Returns:
            Oluşturulan PDF dosyasının yolu
        """
        try:
            logger.info(f"Roadmap PDF oluşturuluyor: {roadmap_data.get('title', 'Unknown')}")
            
            # PDF dosya adını oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            roadmap_title = roadmap_data.get('title', 'roadmap').replace(' ', '_')
            filename = f"roadmap_{roadmap_title}_{timestamp}.pdf"
            filepath = os.path.join(self.output_directory, filename)
            
            # PDF dokümanını oluştur
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # PDF içeriğini oluştur
            story = []
            
            # Başlık sayfası
            story.extend(self._create_title_page(roadmap_data, user_info))
            story.append(PageBreak())
            
            # İçindekiler
            story.extend(self._create_table_of_contents(roadmap_data))
            story.append(PageBreak())
            
            # Roadmap içeriği
            story.extend(self._create_roadmap_content(roadmap_data))
            
            # PDF'i oluştur
            doc.build(story)
            
            logger.info(f"PDF başarıyla oluşturuldu: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"PDF oluşturma hatası: {e}")
            raise
    
    def _create_title_page(self, 
                          roadmap_data: Dict[str, Any],
                          user_info: Optional[Dict[str, Any]] = None) -> List:
        """Başlık sayfası oluşturur"""
        story = []
        
        # Ana başlık
        title = roadmap_data.get('title', 'Roadmap')
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        # Açıklama
        description = roadmap_data.get('description', '')
        if description:
            story.append(Paragraph("Açıklama:", self.styles['CustomHeading2']))
            story.append(Paragraph(description, self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Hedefler
        goals = roadmap_data.get('goals', [])
        if goals:
            story.append(Paragraph("Hedefler:", self.styles['CustomHeading2']))
            for goal in goals:
                story.append(Paragraph(f"• {goal}", self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Kullanıcı bilgileri
        if user_info:
            story.append(Paragraph("Kullanıcı Bilgileri:", self.styles['CustomHeading2']))
            user_text = f"Ad: {user_info.get('name', 'N/A')}<br/>"
            user_text += f"E-posta: {user_info.get('email', 'N/A')}<br/>"
            user_text += f"Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            story.append(Paragraph(user_text, self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Roadmap bilgileri
        story.append(Paragraph("Roadmap Bilgileri:", self.styles['CustomHeading2']))
        roadmap_info = f"Toplam Modül Sayısı: {len(roadmap_data.get('modules', []))}<br/>"
        roadmap_info += f"Tahmini Süre: {roadmap_data.get('estimated_duration', 'N/A')}<br/>"
        roadmap_info += f"Zorluk Seviyesi: {roadmap_data.get('difficulty', 'N/A')}"
        story.append(Paragraph(roadmap_info, self.styles['CustomBody']))
        
        return story
    
    def _create_table_of_contents(self, roadmap_data: Dict[str, Any]) -> List:
        """İçindekiler sayfası oluşturur"""
        story = []
        
        story.append(Paragraph("İçindekiler", self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        modules = roadmap_data.get('modules', [])
        for i, module in enumerate(modules, 1):
            module_title = module.get('title', f'Modül {i}')
            story.append(Paragraph(f"{i}. {module_title}", self.styles['CustomBody']))
        
        return story
    
    def _create_roadmap_content(self, roadmap_data: Dict[str, Any]) -> List:
        """Roadmap içeriğini oluşturur"""
        story = []
        
        modules = roadmap_data.get('modules', [])
        
        for i, module in enumerate(modules, 1):
            # Modül başlığı
            module_title = module.get('title', f'Modül {i}')
            story.append(Paragraph(f"{i}. {module_title}", self.styles['ModuleTitle']))
            
            # Modül açıklaması
            module_description = module.get('description', '')
            if module_description:
                story.append(Paragraph(module_description, self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            # Modül kaynakları
            resources = module.get('resources', [])
            if resources:
                story.append(Paragraph("Kaynaklar:", self.styles['CustomHeading2']))
                for resource in resources:
                    story.append(Paragraph(f"• {resource}", self.styles['ResourceStyle']))
                story.append(Spacer(1, 10))
            
            # Modül görevleri
            tasks = module.get('tasks', [])
            if tasks:
                story.append(Paragraph("Görevler:", self.styles['CustomHeading2']))
                for task in tasks:
                    story.append(Paragraph(f"• {task}", self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            # Modül notları
            notes = module.get('notes', '')
            if notes:
                story.append(Paragraph("Notlar:", self.styles['CustomHeading2']))
                story.append(Paragraph(notes, self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            story.append(Spacer(1, 20))
        
        return story
    
    def generate_progress_report_pdf(self, 
                                   progress_data: Dict[str, Any],
                                   user_info: Optional[Dict[str, Any]] = None) -> str:
        """
        İlerleme raporu PDF'i oluşturur
        
        Args:
            progress_data: İlerleme verisi
            user_info: Kullanıcı bilgileri
            
        Returns:
            Oluşturulan PDF dosyasının yolu
        """
        try:
            logger.info("İlerleme raporu PDF oluşturuluyor")
            
            # PDF dosya adını oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"progress_report_{timestamp}.pdf"
            filepath = os.path.join(self.output_directory, filename)
            
            # PDF dokümanını oluştur
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            story = []
            
            # Başlık
            story.append(Paragraph("Öğrenme İlerleme Raporu", self.styles['CustomTitle']))
            story.append(Spacer(1, 30))
            
            # Genel istatistikler
            story.append(Paragraph("Genel İstatistikler", self.styles['CustomHeading2']))
            
            stats_data = [
                ["Metrik", "Değer"],
                ["Toplam Roadmap", str(progress_data.get('total_roadmaps', 0))],
                ["Tamamlanan Modül", str(progress_data.get('total_completed_modules', 0))],
                ["Toplam Süre", f"{progress_data.get('total_time_spent_minutes', 0)} dakika"],
                ["Tamamlanma Oranı", f"%{progress_data.get('overall_completion_rate', 0)}"]
            ]
            
            stats_table = Table(stats_data, colWidths=[200, 100])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Roadmap detayları
            roadmaps = progress_data.get('roadmaps', [])
            if roadmaps:
                story.append(Paragraph("Roadmap Detayları", self.styles['CustomHeading2']))
                
                for roadmap in roadmaps:
                    roadmap_title = f"Roadmap #{roadmap.get('roadmap_id', 'N/A')}"
                    story.append(Paragraph(roadmap_title, self.styles['ModuleTitle']))
                    
                    roadmap_info = f"İlerleme: %{roadmap.get('overall_progress', 0)}<br/>"
                    roadmap_info += f"Tamamlanan: {roadmap.get('completed_modules', 0)}/{roadmap.get('total_modules', 0)}<br/>"
                    roadmap_info += f"Süre: {roadmap.get('total_time_spent_minutes', 0)} dakika"
                    
                    story.append(Paragraph(roadmap_info, self.styles['CustomBody']))
                    story.append(Spacer(1, 10))
            
            # PDF'i oluştur
            doc.build(story)
            
            logger.info(f"İlerleme raporu PDF oluşturuldu: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"İlerleme raporu PDF oluşturma hatası: {e}")
            raise
    
    def generate_learning_summary_pdf(self, 
                                    summary_data: Dict[str, Any],
                                    user_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Öğrenme özeti PDF'i oluşturur
        
        Args:
            summary_data: Özet verisi
            user_info: Kullanıcı bilgileri
            
        Returns:
            Oluşturulan PDF dosyasının yolu
        """
        try:
            logger.info("Öğrenme özeti PDF oluşturuluyor")
            
            # PDF dosya adını oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"learning_summary_{timestamp}.pdf"
            filepath = os.path.join(self.output_directory, filename)
            
            # PDF dokümanını oluştur
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            story = []
            
            # Başlık
            story.append(Paragraph("Öğrenme Özeti", self.styles['CustomTitle']))
            story.append(Spacer(1, 30))
            
            # Öğrenilen konular
            topics = summary_data.get('learned_topics', [])
            if topics:
                story.append(Paragraph("Öğrenilen Konular", self.styles['CustomHeading2']))
                for topic in topics:
                    story.append(Paragraph(f"• {topic}", self.styles['CustomBody']))
                story.append(Spacer(1, 20))
            
            # Başarılar
            achievements = summary_data.get('achievements', [])
            if achievements:
                story.append(Paragraph("Başarılar", self.styles['CustomHeading2']))
                for achievement in achievements:
                    story.append(Paragraph(f"🏆 {achievement}", self.styles['CustomBody']))
                story.append(Spacer(1, 20))
            
            # Gelecek hedefler
            future_goals = summary_data.get('future_goals', [])
            if future_goals:
                story.append(Paragraph("Gelecek Hedefler", self.styles['CustomHeading2']))
                for goal in future_goals:
                    story.append(Paragraph(f"🎯 {goal}", self.styles['CustomBody']))
                story.append(Spacer(1, 20))
            
            # PDF'i oluştur
            doc.build(story)
            
            logger.info(f"Öğrenme özeti PDF oluşturuldu: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Öğrenme özeti PDF oluşturma hatası: {e}")
            raise
    
    def cleanup_old_pdfs(self, days_to_keep: int = 7):
        """Eski PDF dosyalarını temizler"""
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
            
            deleted_count = 0
            for filename in os.listdir(self.output_directory):
                if filename.endswith('.pdf'):
                    filepath = os.path.join(self.output_directory, filename)
                    if os.path.getmtime(filepath) < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
            
            logger.info(f"{deleted_count} eski PDF dosyası silindi")
            
        except Exception as e:
            logger.error(f"PDF temizleme hatası: {e}")
    
    def get_pdf_info(self, filepath: str) -> Dict[str, Any]:
        """PDF dosyası hakkında bilgi döndürür"""
        try:
            if not os.path.exists(filepath):
                return {"error": "Dosya bulunamadı"}
            
            file_stats = os.stat(filepath)
            return {
                "filename": os.path.basename(filepath),
                "filepath": filepath,
                "size_bytes": file_stats.st_size,
                "size_mb": round(file_stats.st_size / (1024 * 1024), 2),
                "created_time": datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                "modified_time": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"PDF bilgi alma hatası: {e}")
            return {"error": str(e)}
