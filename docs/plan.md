# Portfolyo revizyonu planı

Başlangıç: 2026-11-12. Bu belge reponun portfolyoya eklenmesi ve Türkçe GTA 5 Shorts üretimi için yapılacak işleri sırayla listeler.

## Amaç

- Repo portfolyoya eklenir: iki dilli README, repo açıklaması, topic'ler, Website alanı, v1.0.0 etiketi ve Release.
- Araç Türkçe GTA 5 Shorts üretebilir hale gelir: senaryoyu Gemini yazar, Edge TTS seslendirir, görüntü hazır oynanış videosundan alınır.

## Kararlar

- Ayrı bir repo açılmaz, bu repo geliştirilir.
- Dil Türkçe. Görüntü kaynağı kullanıcının eklediği hazır oynanış videolarıdır; video indirme özelliği yapılmaz.
- Kökteki 69 senaryo dosyası, `brands`, `.cursor` ve `scripts` klasörleri ve eski kanallara ait 4 konu listesi yedeklenip repodan silindi. `senaryo.example.json` şablon olarak kaldı; çalışma kopyası `senaryo.json` git dışında tutulur.
- Eski kanalların koddaki marka profilleri ve biçimleri, yani paint, file, drawn ve pov, özellik olarak kalır. GTA paketi marka profili olarak değil, komut satırında ayrı bir biçim olarak eklendi: `--format gta` ve `VIDEO_FORMAT=gta`. Marka profilleri yalnız paint biçiminin Studio dosyasında kullanılıyor.
- Senaryoyu Gemini ücretsiz katmanda yazar. Google Search doğrulaması yeni anahtarlarda ücretli olduğu için kapalı. GTA bilgilerini Claude en az iki bağımsız kaynakla doğrulayıp `scenarios/topics-gta.json` dosyasına kaynaklarıyla yazar; Gemini yalnız verilen bilgiyi Shorts metnine çevirir, kurallara uymayan metni kod geri gönderir.
- Ses `tr-TR-AhmetNeural`, Shorts'ta kelime vurgulu altyazı. Kullanıcı kararı, 2026-11-12.
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
6. **feat/gemini-scripts ve fix/gemini-free-tier:** `IScriptGenerator` için Gemini. Ücretsiz modeller sırayla denenir, biri meşgulse sıradaki yazar. Google Search doğrulaması seçenek olarak kaldı; açıkken kaynaklar senaryo dosyasına yazılır ama seslendirilmez. Anahtar `.env` içinde, Ollama seçenek olarak kalır.
7. **feat/shorts-karaoke ve feat/gta-shorts-tr:** Shorts'ta konuşulan kelimeyi vurgulayan altyazı. Türkçe GTA 5 Shorts paketi: kaynaklı 11 bilgilik liste; yalnız verilen bilgiyi yazan istem; uzunluk, abartılı söz, bilgide olmayan sayı ve Türkçe yazım denetimi; Ahmet sesi; oynanış videosu; sahne sonundaki sessizliğin kırpılması; `generate`, `daily` ve `topics` için `--format gta`.
8. **fix/final-scan, son tarama:** güvenlik kuralları ve kenar durumlar. Git geçmişinde anahtar yok, kod kabuk komutu ve `eval` kullanmıyor. 13 bulgu düzeltildi:
   - Pillow 11.3'te bilinen açıklar var ve MoviePy 2.2.1 Pillow'u 12'nin altında tutuyor. Dışarıdan gelen görseller yalnız JPEG, PNG ve WebP olarak açılıyor.
   - Stok görüntü katkıcıları YouTube açıklamasına hiç gitmiyordu, artık yüklemeyle gidiyor.
   - Hata metni manifest'e maskesiz yazılıyordu; Pixabay anahtarı URL içinde olduğu için sızabilirdi.
   - Paint kapakları sabit bir Cursor yolunda aranıyordu, artık `output/storyboard` klasöründe.
   - Gizli yükleme kilidi yanlış sebebe bağlanıyordu. Doğrusu, denetimden geçmemiş API projesi.
   - `clean` onay sormadan siliyordu ve proje kökünü de silebiliyordu.
   - İndirmelerde sayfa türü ve üst boyut denetimi yoktu.
   - `schedule --remove` Türkçe Windows'ta hata veriyordu.
   - `doctor` GTA biçimini bilmiyordu.
   - `utils` ve `config` arasında döngüsel import vardı.
   - Testler geliştiricinin `.env` dosyasını okuyordu.
   - ffmpeg altyazı filtresi kesme işaretli yolda bozuluyordu.
   - Yazı tipi indirmeleri sabit SHA-256 özetleriyle doğrulanmıyordu.
   Sanal ortamdaki pip'i kullanıcı yükseltir. README bulguları iş 9'da.
9. **docs/readme:** iki dilli README ve Öğrendiklerim bölümü.
   - README.md İngilizce, README.tr.md Türkçe olarak şablona göre yeniden yazıldı. Ekran görüntüsü olarak kelime vurgulu altyazının GIF'i ve `topics --gta` çıktısının SVG'si `docs/media` klasöründe. GIF'teki arka plan, repoda oyun görüntüsü olmadığı için üretilmiş bir renk geçişi.
   - Eski bilgiler düzeltildi: YouTube'da günde yaklaşık altı yükleme sınırı yok, `videos.insert` için ayrı bir günlük 100 yükleme kotası var. Gemini eklendiği için araç artık tamamen yerel değil; komut satırı, Makefile ve pyproject açıklamaları buna göre değişti.
10. **Yayın:** repo açıklaması, topic'ler ve Website alanı; `docs/seo.md` ve portfolyo sayfası; v1.0.0 etiketi ve Release; proje notları; portfolyo kartı metinleri ve `docs/showcase.png`.
