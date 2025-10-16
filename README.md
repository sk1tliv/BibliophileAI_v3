# BibliophileAi
Bu proje, kullanıcılara doğal dil ile sohbet ederek kişisel kitap önerileri sunan modern bir web uygulamasıdır. Streamlit ile geliştirilen arayüzü, SQLite veritabanı yönetimi ve OpenAI GPT tabanlı generative AI motoruyla zenginleştirilmiştir. Ayrıca, bilgiye dayalı ve güncel yanıtlar sunmak için Retrieval-Augmented Generation (RAG) mimarisi esas alınmıştır.

---

## Uygulama Akışı ve Özellikler

1. **Kullanıcı Girişi / Kayıt:** Sol panelde kolayca yeni hesap açın veya mevcut hesabınızla giriş yapın. Kimlik doğrulama işlemleri SQLite veritabanında güvenli şekilde tutulur.
2. **Favori Kitaplar:** Başarılı giriş sonrası, favori kitap listeniz sol panelde gösterilir.
3. **Kitap Sorgusu ve Tavsiye:** Arama kutusuna doğal dilde bir istek yazın (örn. "Tarihi romanlardan uygun fiyatlı öneri" veya "kısa polisiye kitap tavsiyesi"). Sistem, hem LLM’den hem de veri setlerinden filtrelenmiş sonuçlar döndürür.
4. **Filtreleme:** Fiyat ve sayfa sayısı için görsel slider ile iyileştirilmiş filtreleme.
5. **Detaylı Kartlar:** Kitap adı, yazar, yayıncı, fiyat, açıklama ve satın alma linkleri ile gösterilir.
6. **Favorilere Ekleme:** Sunulan önerilerden herhangi biri tek tıkla favorilere eklenebilir.

---

# Kullanılan Veri Setleri
Projede kitap öneri sisteminin güvenilir ve kapsamlı çalışması için iki ayrı Kaggle veri seti kullanılmıştır :

1. **Turkish Book Dataset** (yusufsadpc)
Kaynak: Kaggle - Turkish Book Dataset
Bu veri seti, Türkiye’de yayınlanmış binlerce kitap hakkında başlık, yazar, yayıncı, sayfa sayısı, tür, ISBN, açıklama ve fiyat gibi ayrıntılı bilgiler içerir. Kitaplar çeşitli türlere (roman, polisiye, biyografi, tarih vb.) göre kategorize edilmiştir ve kullanıcıların zengin bir arama/filtreleme yapmasını sağlar.

2. **Turkish Book Data Set** (muhammedbrahimtop)
Kaynak: Kaggle - Turkish Book Data Set
Bu veri seti, farklı yayınevlerine ait kitapların detaylarını sunar; kitap adı, yazar, basım yılı, tür, yayıncı, fiyat, ortalama puan ve satılma sayısı gibi bilgileri içerir. Kitap tavsiye ve analiz işlemleri için verimli bir kaynak sunar.

---

## Proje Yapısı

├── venv/ 
├── .gitignore 
├── .env # OpenAI API anahtarı ve hassas bilgiler
├── app.py 
├── requirements.txt # Proje bağımlılıkları
├── users.db # SQLite veritabanı (kullanıcı ve favori kitaplar)
├── tum_kitaplar.csv # Kitap veri seti (büyük katalog)
├── TurkishBookDataSet.csv # Türkçe kitap veri seti (detaylı içerik)

---

## Kurulum ve Çalıştırma

1. Paket kurulumları:
    ```
    pip install streamlit pandas sqlite3 openai python-dotenv
    ```
2. `.env` dosyasına OpenAI API anahtarınızı ekleyin:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```
3. Veri dosyalarını proje dizinine ekleyin.
4. Uygulamayı başlatın:
    ```
    streamlit run app.py
    ```

---

# Projeden Görseller 
<img src="./dosya_yapisi.png" alt="Proje Dosya Yapısı" width="200"/>
