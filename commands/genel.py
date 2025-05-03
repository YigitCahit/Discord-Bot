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
            title="Bot Komutları",
            description="İşte kullanabileceğiniz komutlar:",
            color=discord.Color.blue()
        )
        embed.add_field(name="/genel ping", value="Bot gecikmesini gösterir", inline=False)
        embed.add_field(name="/genel merhaba", value="Bot size selam verir", inline=False)
        embed.add_field(name="/genel yardım", value="Bu yardım mesajını gösterir", inline=False)
        embed.add_field(name="/sunucu bilgi", value="Sunucu bilgilerini gösterir", inline=False)
        embed.add_field(name="/kullanıcı avatar", value="Kullanıcının avatarını gösterir", inline=False)
        embed.add_field(name="/moderasyon temizle", value="Belirtilen sayıda mesajı siler", inline=False)
        embed.add_field(name="/moderasyon at", value="Bir kullanıcıyı sunucudan atar", inline=False)
        embed.add_field(name="/moderasyon yasakla", value="Bir kullanıcıyı sunucudan yasaklar", inline=False)
        embed.set_footer(text=f"Bot Sürümü: 1.0.0 | {datetime.datetime.now().strftime('%d/%m/%Y')}")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(GenelKomutlar(bot))
