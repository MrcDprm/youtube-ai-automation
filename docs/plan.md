# Portfolyo revizyonu planı

Başlangıç: 2026-11-12. Bu belge reponun portfolyoya eklenmesi ve Türkçe GTA 5 Shorts üretimi için yapılacak işleri sırayla listeler.

## Amaç

- Repo portfolyoya eklenir: iki dilli README, repo açıklaması, topic'ler, Website alanı, v1.0.0 etiketi ve Release.
- Araç Türkçe GTA 5 Shorts üretebilir hale gelir: senaryoyu Gemini yazar, Edge TTS seslendirir, görüntü hazır oynanış videosundan alınır.

## Kararlar

- Ayrı bir repo açılmaz, bu repo geliştirilir.
- Dil Türkçe. Görüntü kaynağı kullanıcının eklediği hazır oynanış videolarıdır; video indirme özelliği yapılmaz.
- Kökteki 69 senaryo dosyası, `brands`, `.cursor` ve `scripts` klasörleri ve eski kanallara ait 4 konu listesi yedeklenip repodan silindi. `senaryo.example.json` şablon olarak kaldı; çalışma kopyası `senaryo.json` git dışında tutulur.
- Eski kanalların koddaki marka profilleri ve biçimleri, yani paint, file, drawn ve pov, özellik olarak kalır. GTA paketi aynı marka sistemine eklenir.
- Cursor ortak yazar satırı olan 3 commit olduğu gibi kalır, geçmiş yeniden yazılmaz.
- Araç komut satırında kalır; arayüz ve kurulum dosyası yapılmaz.
- YouTube'a yükleme özelliği kalır. API ile yüklenen videolar Google denetiminden geçmemiş projelerde gizli olarak kilitlendiği için günlük yayın YouTube Studio'dan zamanlanır.
- README'de somut çıktısı olmayan bölümler, örneğin ekran görüntüsü, boş kalabilir.

## Başlangıç durumu

- 361 testin 18'i kırıktı. 17'sinde test sahtesi `FakeEditor`'a `build_zenn_story` eklenmemiş, 1'inde paint senaryosu `brand_id` damgalamıyor.
- ruff 61 hata veriyor, 15 dosya biçim dışı, mypy 4 hata buluyor. README'deki `make check` temiz değil.
- edge-tts 7.2.8 Microsoft sunucusundan 403 alıyor, 7.3.1 çalışıyor.
- Senaryo üretimi yalnızca Ollama ile çalışıyor, Ollama da bu bilgisayardan kaldırıldı.
- Altyazıda büyük harf seçeneği `str.upper` kullanıyor; i harfi İ yerine I oluyor.
- `modules/pipeline.py` içinde bu bilgisayara ait sabit bir Cursor klasör yolu var.

## İşler

Her iş kendi branch'inde, küçük commit'lerle yapılır; her commit'te testler geçer.

1. **chore/remove-channel-content:** bu plan, eski kanal içeriğinin silinmesi, silinen dosyaları okuyan iki testin kendi geçici dosyasını kurması.
2. **fix/green-build:** 18 kırık test, mypy, ruff ve biçim hataları; `make check` temiz.
3. **fix/turkish-uppercase:** altyazı ve kapak metninde Türkçe büyük harf, testleriyle.
4. **fix/edge-tts-403:** en düşük edge-tts sürümü 7.3.1; 403 gelince paketi güncellemeyi öneren anlaşılır hata.
5. **feat/gameplay-background:** uzun oynanış videolarından her videoya daha önce kullanılmamış bir kesit seçen görüntü kaynağı; 9:16 kırpma, oyun sesi kısık, kullanılan aralıklar önbellekte.
6. **feat/gemini-scripts:** `IScriptGenerator` için Gemini. Bilgiler Google Search ile doğrulanır, kaynaklar senaryo dosyasına yazılır ama seslendirilmez. Anahtar `.env` içinde, Ollama seçenek olarak kalır.
7. **feat/gta-shorts-tr:** Türkçe GTA 5 Shorts paketi: kuralların Türkçeye ve hazır arka plana uyarlanmış hali, konu listesi, ses, altyazı ve kapak ayarları.
8. **Son tarama:** güvenlik kuralları ve kenar durumlar. Bilinen bulgular: sabit Cursor yolu, karaoke altyazıda ters bölü kaçışı, README'de API yüklemesinin gizli kilitlendiği bilgisinin eksik olması, bağımlılık taraması.
9. **docs/readme:** iki dilli README ve Öğrendiklerim bölümü.
10. **Yayın:** repo açıklaması, topic'ler ve Website alanı; `docs/seo.md` ve portfolyo sayfası; v1.0.0 etiketi ve Release; proje notları; portfolyo kartı metinleri ve `docs/showcase.png`.
