import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Bot için gerekli izinleri ayarla
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot istemcisini oluştur
class DiscordBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self) -> None:
        # Komut modüllerini yükle
        for module in ["genel", "sunucu", "kullanici", "moderasyon", "rank"]:
            module_path = f"commands.{module}"
            try:
                await self.load_extension(module_path)
                print(f"{module_path} modülü yüklendi.")
            except Exception as e:
                print(f"{module_path} modülü yüklenirken hata oluştu: {e}")
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            # Komutları global olarak senkronize et
            await self.tree.sync()
            self.synced = True
        
        # Bot durumunu ayarla
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="/genel yardım | Yardım"
        ))
        
        print(f"Bot olarak giriş yapıldı: {self.user.name}")
        print(f"Bot ID: {self.user.id}")
        print(f"Discord.py sürümü: {discord.__version__}")
        print("Bot hazır!")

# Discord.py uzantılarını desteklemek için gerekli fonksiyon
async def load_extension(self, name: str):
    module = __import__(name, fromlist=["setup"])
    await module.setup(self)

# Discord.Client sınıfına load_extension metodunu ekle
discord.Client.load_extension = load_extension

# Botu oluştur ve çalıştır
if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        print("HATA: .env dosyasında TOKEN değişkeni bulunamadı!")
    else:
        bot = DiscordBot()
        bot.run(token)
