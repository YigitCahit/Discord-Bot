import discord
from discord import app_commands
import datetime

class GenelKomutlar(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name="genel", description="Genel komutlar")
        self.bot = bot
    
    @app_commands.command(name="ping", description="Bot gecikmesini gösterir")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Gecikme: {round(self.bot.latency * 1000)}ms")
        
    @app_commands.command(name="merhaba", description="Bot size merhaba der")
    async def merhaba(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Merhaba {interaction.user.mention}! Nasılsın?")
        
    @app_commands.command(name="yardım", description="Komutlar hakkında bilgi alın")
    async def yardim(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Bot Yardım Menüsü",
            description="Tüm komutlar slash komut (/) ile başlar. Detaylı bilgi için kategorilere göz atın:",
            color=discord.Color.blue()
        )
        
        # Genel Komutlar
        embed.add_field(
            name="📌 Genel Komutlar",
            value=(
                "`/genel ping` - Bot gecikmesini gösterir\n"
                "`/genel merhaba` - Bot size selam verir\n"
                "`/genel yardım` - Bu yardım menüsünü gösterir"
            ),
            inline=False
        )
        
        # Sunucu Komutları
        embed.add_field(
            name="🏠 Sunucu Komutları",
            value=(
                "`/sunucu bilgi` - Sunucu hakkında detaylı bilgi\n"
                "`/sunucu roller` - Sunucudaki tüm rolleri listeler\n"
                "`/sunucu emoji` - Sunucudaki özel emojileri gösterir"
            ),
            inline=False
        )
        
        # Kullanıcı Komutları
        embed.add_field(
            name="👤 Kullanıcı Komutları",
            value=(
                "`/kullanıcı avatar [kullanıcı]` - Avatar görüntüleme\n"
                "`/kullanıcı bilgi [kullanıcı]` - Kullanıcı profili ve istatistikleri"
            ),
            inline=False
        )
        
        # Moderasyon Komutları
        embed.add_field(
            name="🛡️ Moderasyon Komutları",
            value=(
                "`/moderasyon temizle <miktar>` - Mesaj silme\n"
                "`/moderasyon at <kullanıcı>` - Kullanıcı atma\n"
                "`/moderasyon yasakla <kullanıcı>` - Kullanıcı yasaklama\n"
                "`/moderasyon yasak_kaldır <id>` - Yasak kaldırma\n"
                "`/moderasyon söyle <kanal> <mesaj>` - Bot ile mesaj gönderme"
            ),
            inline=False
        )
        
        # Rank Sistemi Komutları
        embed.add_field(
            name="🎮 Rank Sistemi Komutları",
            value=(
                "`/rank profil [kullanıcı]` - Seviye profili görüntüleme\n"
                "`/rank liderlik [limit]` - Sunucu liderlik tablosu\n"
                "`/rank rol_ayarla <seviye> <rol>` - Rank rolü ayarlama (Yönetici)\n"
                "`/rank roller` - Tüm rank rollerini görüntüleme"
            ),
            inline=False
        )
        
        embed.add_field(
            name="💡 Özellikler",
            value=(
                "✅ Çoklu sunucu desteği\n"
                "✅ Otomatik XP kazanma sistemi\n"
                "✅ Seviye atladığında otomatik rol güncelleme\n"
                "✅ Her sunucu için ayrı rank sistemi"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Bot Sürümü: 2.0.0 | Çoklu Sunucu Desteği | {datetime.datetime.now().strftime('%d/%m/%Y')}")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(GenelKomutlar(bot))
