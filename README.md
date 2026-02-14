# 🤖 Discord Bot - Türkçe Çoklu Sunucu Desteği

Modern Discord.py ile geliştirilmiş, slash komutları destekleyen ve çoklu sunucu yapısına sahip profesyonel Türkçe Discord botu.

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Özellikler

- ⚡ **Slash Komutları** - Modern Discord slash komut sistemi
- 🏗️ **Modüler Yapı** - Kolay genişletilebilir ve bakımı yapılabilir
- 🌐 **Çoklu Sunucu Desteği** - Her sunucu için bağımsız rank sistemi
- 🎮 **Rank Sistemi** - XP kazanma, seviye atlama ve otomatik rol atama
- 🛡️ **Moderasyon Araçları** - Mesaj silme, kullanıcı atma/yasaklama
- 💾 **SQLite Veritabanı** - Hızlı ve güvenilir veri saklama
- 📊 **Liderlik Tablosu** - Sunucu bazlı XP sıralaması
- 🎨 **Kullanıcı Dostu** - Türkçe arayüz ve detaylı embed mesajları

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- Discord.py 2.3.0+
- aiosqlite
- python-dotenv

## 🚀 Kurulum

### 1. Projeyi İndirin

```bash
git clone https://github.com/YigitCahit/Discord-Bot.git
cd Discord-Bot
```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Ortam Değişkenlerini Ayarlayın

Proje klasöründe `.env` dosyası oluşturun:

```env
TOKEN=your_discord_bot_token_here
```

### 4. Botu Çalıştırın

```bash
python main.py
```

## 🔑 Bot Token Alma

1. [Discord Developer Portal](https://discord.com/developers/applications)'a gidin
2. **"New Application"** butonuna tıklayın
3. Uygulamanıza bir isim verin ve **"Create"** deyin
4. Sol menüden **"Bot"** sekmesine gidin
5. **"Add Bot"** butonuna tıklayın
6. **"Reset Token"** ile token'ınızı alın
7. Token'ı `.env` dosyasına ekleyin

### Bot İzinleri

Bot'u sunucuya eklerken şu izinleri verin:

- ✅ `applications.commands` - Slash komutları için
- ✅ `Manage Roles` - Rank rolleri vermek için
- ✅ `Kick Members` - Kullanıcı atmak için
- ✅ `Ban Members` - Kullanıcı yasaklamak için
- ✅ `Manage Messages` - Mesaj silmek için
- ✅ `Read Messages/View Channels` - Mesajları okumak için
- ✅ `Send Messages` - Mesaj göndermek için

## 📚 Komutlar

### 🔹 Genel Komutlar

| Komut | Açıklama |
|-------|----------|
| `/genel ping` | Bot'un gecikmesini (latency) gösterir |
| `/genel merhaba` | Bot sizi selamlar |
| `/genel yardım` | Tüm komutlar hakkında bilgi verir |

### 🔹 Sunucu Komutları

| Komut | Açıklama |
|-------|----------|
| `/sunucu bilgi` | Sunucu hakkında detaylı bilgiler |
| `/sunucu roller` | Sunucudaki tüm rolleri listeler |
| `/sunucu emoji` | Sunucudaki özel emojileri gösterir |

### 🔹 Kullanıcı Komutları

| Komut | Açıklama |
|-------|----------|
| `/kullanıcı avatar [kullanıcı]` | Avatarı büyük boyutta gösterir |
| `/kullanıcı bilgi [kullanıcı]` | Kullanıcı profili ve istatistikleri |

### 🔹 Moderasyon Komutları

| Komut | Açıklama | Gerekli İzin |
|-------|----------|--------------|
| `/moderasyon temizle <miktar>` | Belirtilen sayıda mesajı siler | Mesajları Yönet |
| `/moderasyon at <kullanıcı> [sebep]` | Kullanıcıyı sunucudan atar | Üyeleri At |
| `/moderasyon yasakla <kullanıcı> [sebep]` | Kullanıcıyı yasaklar | Üyeleri Yasakla |
| `/moderasyon yasak_kaldır <kullanıcı_id>` | Yasağı kaldırır | Üyeleri Yasakla |
| `/moderasyon söyle <kanal> <mesaj>` | Belirtilen kanala mesaj gönderir | Yönetici |

### 🎮 Rank Sistemi Komutları

| Komut | Açıklama | Gerekli İzin |
|-------|----------|--------------|
| `/rank profil [kullanıcı]` | Seviye profili ve ilerleme çubuğu | - |
| `/rank liderlik [limit]` | Sunucu liderlik tablosu (max 25) | - |
| `/rank rol_ayarla <seviye> <rol>` | Belirli seviye için otomatik rol atar | Yönetici |
| `/rank roller` | Tüm rank rollerini görüntüler | - |

## 🎯 Rank Sistemi

### Nasıl Çalışır?

1. **XP Kazanma**: Kullanıcılar her mesaj attığında 5 XP kazanır (60 saniye cooldown)
2. **Seviye Atlama**: Her seviye için `seviye × 100` XP gerekir
   - Seviye 1: 100 XP
   - Seviye 2: 200 XP
   - Seviye 10: 1000 XP
3. **Otomatik Rol**: Belirli seviyelere ulaşıldığında otomatik roller verilir
4. **Otomatik Rol Güncelleme**: Yeni seviyeye ulaşıldığında önceki rank rolleri otomatik kaldırılır
5. **Çoklu Sunucu**: Her sunucuda ayrı rank sistemi

### Rank Rolleri Ayarlama

Her sunucu başlangıçta boş rank sistemi ile gelir. Roller manuel olarak ayarlanmalıdır:

```
/rank rol_ayarla seviye:5 rol:@Bronze
/rank rol_ayarla seviye:10 rol:@Silver
/rank rol_ayarla seviye:20 rol:@Gold
/rank rol_ayarla seviye:50 rol:@Platinum
```

**Not:** Her sunucu için rollerin ayrı ayrı ayarlanması gerekir.

### Sunucu Başına Ayrı Sistem

✅ Sunucu A'da Level 50 olabilirsiniz
✅ Sunucu B'de Level 1'den başlarsınız
✅ Her sunucu kendi rollerini ayarlar

## 📁 Proje Yapısı

```
Discord-Bot/
├── main.py                 # Ana bot dosyası
├── database.py             # Veritabanı işlemleri
├── requirements.txt        # Python bağımlılıkları
├── .env                    # Ortam değişkenleri (TOKEN)
├── .gitignore             # Git ignore ayarları
├── commands/              # Komut modülleri
│   ├── genel.py           # Genel komutlar
│   ├── sunucu.py          # Sunucu komutları
│   ├── kullanici.py       # Kullanıcı komutları
│   ├── moderasyon.py      # Moderasyon komutları
│   └── rank.py            # Rank sistemi komutları
└── README.md              # Bu dosya
```

## 🗄️ Veritabanı Yapısı

### user_ranks
Her kullanıcının her sunucudaki rank bilgisi
```sql
PRIMARY KEY (user_id, guild_id)
- xp: Toplam XP
- level: Mevcut seviye
- messages: Toplam mesaj sayısı
- last_message_time: Son mesaj zamanı (cooldown için)
```

### rank_roles
Her sunucunun rank rolleri
```sql
PRIMARY KEY (guild_id, level)
- role_id: Verilecek rol ID'si
```

### rank_settings
Sunucu bazlı XP ayarları
```sql
- xp_per_message: Mesaj başına XP (varsayılan: 5)
- xp_cooldown: Cooldown süresi saniye (varsayılan: 60)
- level_up_channel: Level atlama bildirimi kanalı (opsiyonel)
```

## 🔧 Konfigürasyon

### XP Ayarları

Veritabanında `rank_settings` tablosunda sunucu bazlı ayarlanır:

- **xp_per_message**: Mesaj başına verilen XP miktarı
- **xp_cooldown**: XP kazanma aralığı (saniye)
- **level_up_channel**: Level atlama bildirimlerinin gönderileceği kanal

## 🤝 Katkıda Bulunma

1. Bu projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje AGPL v3.0 lisansı altında lisanslanmıştır.

## 🐛 Sorun Bildirme

Bir hata bulduysanız veya öneriniz varsa lütfen [Issues](https://github.com/YigitCahit/Discord-Bot/issues) sayfasından bildirebilirsiniz.

## 👤 Geliştirici

**Yigit Cahit**

- GitHub: [@YigitCahit](https://github.com/YigitCahit)

---

⭐ Bu projeyi faydalı bulduysanız yıldız vermeyi unutmayın!
