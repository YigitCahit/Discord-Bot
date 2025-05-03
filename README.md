# Discord Slash Bot

Discord için geliştirilmiş slash komutlarını destekleyen Türkçe bir bot.

## Özellikler

- Slash komutları (/komut) desteği
- Modüler yapı
- Moderasyon komutları (temizle, at, yasakla, vb.)
- Mesaj gönderme komutu (yöneticiler için)
- Sunucu bilgileri
- Kullanıcı bilgileri
- Rank sistemi (seviye/XP) ve otomatik rol atama
- SQLite veritabanı desteği
- ve daha fazlası!

## Kurulum

1. Bu repo'yu klonlayın veya indirin
2. `pip install -r requirements.txt` komutu ile gerekli paketleri yükleyin
3. `.env` dosyasındaki `TOKEN` değişkenine Discord bot token'ınızı ekleyin
4. `python main.py` komutu ile botu çalıştırın

## Bot Token Alma

1. [Discord Developer Portal](https://discord.com/developers/applications)'a gidin
2. "New Application" butonuna tıklayın
3. Bot için bir isim belirleyin ve "Create" butonuna tıklayın
4. Sol menüden "Bot" sekmesine tıklayın
5. "Add Bot" butonuna tıklayın
6. "Reset Token" butonuna tıklayın ve token'ı kopyalayın
7. Bu token'ı `.env` dosyasına ekleyin

## Bot İzinleri Yapılandırma

Bot'unuzu sunucunuza eklerken aşağıdaki izinlere sahip olduğundan emin olun:

- `applications.commands` (Slash komutları için)
- `bot` (Bot fonksiyonları için)

## Komutlar

Bot şu kategorilerdeki komutları destekler:

### Genel Komutlar

- `/genel ping` - Bot gecikmesini gösterir
- `/genel merhaba` - Bot size merhaba der
- `/genel yardım` - Komutlar hakkında bilgi alır

### Sunucu Komutları

- `/sunucu bilgi` - Sunucu hakkında bilgiler
- `/sunucu roller` - Sunucudaki rolleri listeler
- `/sunucu emoji` - Sunucudaki emojileri listeler

### Kullanıcı Komutları

- `/kullanıcı avatar` - Kullanıcının avatarını gösterir
- `/kullanıcı bilgi` - Kullanıcı hakkında bilgi gösterir

### Moderasyon Komutları

- `/moderasyon temizle` - Belirtilen sayıda mesajı siler
- `/moderasyon at` - Bir kullanıcıyı sunucudan atar
- `/moderasyon yasakla` - Bir kullanıcıyı yasaklar
- `/moderasyon yasak_kaldır` - Bir kullanıcının yasağını kaldırır
- `/moderasyon söyle` - Bot aracılığıyla belirtilen kanala mesaj gönderir (yönetici yetkisi gerektirir)

### Rank Sistemi Komutları

- `/rank profil` - Kullanıcının seviye profilini gösterir
- `/rank liderlik` - Sunucudaki seviye liderlik tablosunu gösterir
- `/rank rol_ayarla` - Belirli bir seviye için otomatik rol atar (yönetici yetkisi gerektirir)
- `/rank roller` - Tüm seviye rollerini görüntüler
- `/rank kurulum` - Rank sistemini otomatik olarak kurar (yönetici yetkisi gerektirir)

## Rank Sistemi Kullanımı

Bot, kullanıcılar mesaj attıkça XP kazanır ve belirli seviyelere ulaştığında otomatik olarak roller verilir.
Roller şu şekilde ayarlanabilir:

- `/rank kurulum` komutunu kullanarak varsayılan rol ayarlarını kullanabilirsiniz:
  - Level 1: Bronz (ID: 1358033154291667036)
  - Level 5: Gümüş (ID: 1358033389332074669) 
  - Level 10: Platin (ID: 1358033879319183370)
  - Level 15: Altın (ID: 1358033965952274565)
  - Level 20: Elmas (ID: 1358034021375807529)

- Ya da `/rank rol_ayarla` komutunu kullanarak kendi rol ayarlarınızı yapabilirsiniz.

## Katkıda Bulunma

1. Bu repo'yu fork edin
2. Yeni özellikler ekleyin veya hataları düzeltin
3. Pull request gönderin

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
