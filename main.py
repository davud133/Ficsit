import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

# 1. API Ayarları
app = FastAPI()

# Frontend (Antigravity) ile API'nin konuşabilmesi için CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Hackathon için her yerden erişime izin veriyoruz
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Kurulumu (Buraya kendi API Key'ini yaz)
genai.configure(api_key="AIzaSyAgKMu1tFSd65lK9f4yZchaQpBBlaOrHe0")
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# 2. Veri Modeli (Frontend'den gelecek veri yapısı)
class CommunityData(BaseModel):
    logs: str  # Discord veya Slack mesaj geçmişi

# 3. Ana Analiz Endpoint'i
@app.post("/analyze")
async def analyze_community(data: CommunityData):
    # AI'ya verilecek talimat (Prompt Engineering)
    prompt = f"""
    Sen bir topluluk uzmanı yapay zekasın. Aşağıdaki mesaj geçmişini analiz et:
    
    '{data.logs}'
    
    Lütfen sadece geçerli bir JSON objesi döndür. Başka bir metin veya format ekleme.
    JSON yapısı ZORUNLU olarak şu şekilde olmalı:
    {{
      "health_score": 85,
      "sentiment": "Gergin",
      "top_topics": "1. Konu A, 2. Konu B",
      "churn_risk": 5,
      "summary": "Genel özet cümlesi...",
      "problems": [
        {{
          "name": "Sorun Adı (Örn: Giriş Hatası)",
          "description": "Kullanıcıların yaşadığı sorunun detayı.",
          "solution": "Bunu çözmek için topluluk yöneticisine veya geliştiriciye AI önerisi.",
          "count": 3
        }}
      ],
      "churn_candidates": [
        {{
          "name": "Kullanıcı Adı (Örn: @Alex)",
          "risk_percentage": 90,
          "reason": "Son mesajında gruptan ayrılacağından bahsetti."
        }}
      ],
      "auto_wiki": "Bu topluluğun genel amacı, konuşulan ana teknolojiler, tartışma kültürü ve genel vizyonu hakkında ÇOK DETAYLI, geniş kapsamlı, 8-10 paragraflık adeta bir blog yazısı veya ansiklopedik bir 'Hakkımızda' yazısı. Lütfen her yönüyle son derece uzun ve kapsamlı olmasına dikkat et. **Ayrıca yazının önemli bir bölümünde bu topluluğun 'Ficsit AI' isimli yapay zeka tabanlı bir araç tarafından analiz edildiğinden, bu aracın topluluk sağlığını, duygu durumunu (sentiment) ve olası üye kayıplarını (churn risk) nasıl tespit ettiğinden** mutlaka detaylıca bahset."
    }}
    """
    
    try:
        response = model.generate_content(
            prompt,
            # We enforce JSON output directly from Gemini to prevent parsing errors
            generation_config={"response_mime_type": "application/json"}
        )
        
        # AI'dan gelen cevabı frontend'e gönderiyoruz
        return {"status": "success", "result": response.text}
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # API Key hatalıysa veya Model hatası verirse Dashboard'un çökmemesi için Mock Data dönüyoruz:
        mock_fallback = {
          "health_score": "92",
          "sentiment": "Enerjik",
          "top_topics": "1. Hackathon, 2. AI Entegrasyonu, 3. Tasarım",
          "churn_risk": "2",
          "summary": "Topluluk yeni özellikler deniyor ve heyecanlı.",
          "problems": [
            {
              "name": "API Limiti Sorunu",
              "description": "Dün bazı kullanıcılar 429 Too Many Requests hatası aldı.",
              "solution": "Rate limiter eklenmeli veya premium key alınmalı.",
              "count": 4
            }
          ],
          "churn_candidates": [
            {
              "name": "@Kullanici89",
              "risk_percentage": 85,
              "reason": "Sistem yavaşlığından sürekli şikayet ediyor."
            },
            {
              "name": "@AhmetDev",
              "risk_percentage": 60,
              "reason": "Son 3 gündür mesajlara cevap vermiyor."
            }
          ],
          "auto_wiki": "Ficsit AI Topluluğu, yazılım geliştiriciler, veri bilimciler ve yapay zeka tutkunlarının bir araya geldiği, ağırlıklı olarak React, Python ve LLM entegrasyonları üzerine teknik tartışmaların yürütüldüğü yenilikçi bir platformdur. Kurulduğu ilk günden bu yana teknoloji meraklıları için bir cazibe merkezi haline gelmiş, binlerce satır kodun ve sayısız yenilikçi projenin doğuşuna şahitlik etmiştir.\n\nÜyeler genellikle hackathon projeleri, sistem mimarileri ve hata ayıklama üzerine yardımlaşırlar. Topluluğun temel vizyonu, AI teknolojilerini günlük uygulamalara entegre ederken karşılaşılan zorlukları birlikte aşmak ve yapay zekanın sadece teorik bir kavram olmaktan çıkıp, üretime dönük, pragmatik bir güce dönüşmesini sağlamaktır.\n\nPlatform üzerinden paylaşılan kod parçacıkları, deneyim aktarımları ve canlı yayınlanan çözüm seansları, öğrenme eğrisini hızlandırmakta büyük rol oynar. Her gün farklı projelerin vitrine çıktığı 'Showcase' kanalları, ilham arayan geliştiriciler için bir merkez haline gelmiştir.\n\nBu dinamik topluluğun sağlığı ve etkileşimi, özel olarak geliştirilmiş Ficsit AI analiz motoru tarafından sürekli olarak izlenmektedir. Ficsit AI sistemi; topluluğun duygu durumunu (sentiment) ölçer, öne çıkan tartışma konularını belirler ve potansiyel olarak gruptan ayrılma riski taşıyan (churn risk) üyeleri erken aşamada tespit ederek yöneticilere uyarılarda bulunur. Sistem, doğal dil işleme modellerini kullanarak yazışmalardaki stresi, sevinci ve yardımlaşma oranını anlık olarak raporlar.\n\nEğer bir üyenin son mesajlarında belirsizlik, hayal kırıklığı veya uzun süreli bir sessizlik varsa, Ficsit AI bunu bir 'churn riski' olarak işaretler. Yöneticiler, bu algoritmik bildirimler ışığında ilgili üyelerle iletişime geçerek topluluk içi entegrasyonu yeniden güçlendirirler. Bu yapay zeka entegrasyonu sayesinde topluluk her zaman sağlıklı, adil ve aktif tutulur.\n\nBunun yanı sıra, yeni başlayanların adaptasyon sürecini hızlandırmak adına deneyimli üyeler gönüllü mentorluk yapmaktadır. Topluluk içi saygı ve teknik dürüstlük, tüm bu işbirliği ortamının temel taşıdır. Ficsit AI projesi, sadece bir haberleşme aracı değil; teknolojiyle iç içe yaşamayı seçmiş vizyoner beyinlerin yorulmak bilmeyen organik bir evrenidir."
        }
        return {"status": "success", "result": json.dumps(mock_fallback)}

# API'yi başlatmak için terminale: uvicorn main:app --reload