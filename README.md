# BibliophileAI - RAG Tabanlı Kitap Öneri Chatbotu

BibliophileAI, kitap bilgilerini ve önerilerini akıllı bir şekilde sunan **RAG (Retrieval-Augmented Generation)** tabanlı bir chatbot uygulamasıdır.  
Proje, **Flask**, **Google Gemini**, **LangChain**, ve **Bootstrap** teknolojileriyle geliştirilmiştir.

---

## Örnek Görüntü ve Video

[![Chatbot Demo Video](https://img.youtube.com/vi/DuxALgXKrFc/0.jpg)](https://www.youtube.com/watch?v=DuxALgXKrFc)

---

## Özellikler

- Kitap Bilgisi Arama  
  CSV veri setlerinden kitap başlığına göre anlık arama yapar.

- RAG Entegrasyonu  
  Chroma vector store ve Google Generative AI kullanılarak metin benzerliğine dayalı akıllı yanıt üretimi.

- Gemini 2.0 Flash Modeli  
  Google’ın son nesil LLM modelinden doğal ve tutarlı cevaplar üretir.

- Çoklu Dataset Desteği  
  `data/` klasöründe bulunan birden fazla Türkçe kitap veri setini birleştirir.

---

## Kullanılan Teknolojiler

| Alan | Teknoloji |
|------|------------|
| Backend | Python |
| LLM API | Google Gemini (Generative AI SDK) |
| Frontend | HTML, CSS, Bootstrap |

---

## Kurulum

1. Gerekli paketleri yükle
2. .env dosyası oluştur
3. `.env` dosyasına Google API anahtarını ekle
4. Uygulamayı başlat

---

## Proje Yapısı

bibliophileai/
├── app.py
├── data/
│ ├── books.csv
│ ├── Turkish_Book_Dataset_Kaggle_V2.csv
│ ├── final_csv.csv
│ ├── ...
├── templates/
│ └── index.html
├── .env
├── requirements.txt
└── README.md

---
