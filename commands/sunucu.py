import discord
from discord import app_commands

class SunucuKomutlar(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name="sunucu", description="Sunucu ile ilgili komutlar")
        self.bot = bot
    
    @app_commands.command(name="bilgi", description="Sunucu hakkında bilgi alın")
    async def bilgi(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"{guild.name} Bilgileri",
            description=f"ID: {guild.id}",
            color=discord.Color.green()
        )
        
        # Sunucu özellikleri
        embed.add_field(name="Oluşturulma Tarihi", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Sahibi", value=guild.owner.mention if guild.owner else "Bilinmiyor", inline=True)
        embed.add_field(name="Üye Sayısı", value=guild.member_count, inline=True)
        embed.add_field(name="Metin Kanalları", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Ses Kanalları", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Roller", value=len(guild.roles), inline=True)
        
        # Sunucu resmi
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roller", description="Sunucudaki rolleri listeler")
    async def roller(self, interaction: discord.Interaction):
        guild = interaction.guild
        roles = guild.roles
        
        embed = discord.Embed(
            title=f"{guild.name} Rolleri",
            description=f"Toplam {len(roles)} rol bulunuyor",
            color=discord.Color.gold()
        )
        
        # Rolleri sırala (en yüksek yetkiye sahip olanlar önce)
        # SequenceProxy nesnesi sort metodunu desteklemediği için sorted() kullan
        sorted_roles = sorted(roles, reverse=True)
        
        # Rolleri 3'er gruplar halinde listele
        role_text = ""
        for i, role in enumerate(sorted_roles[1:], 1):  # @everyone rolünü hariç tutuyoruz
            role_text += f"`{role.name}` "
            if i % 3 == 0:
                role_text += "\n"
        
        embed.add_field(name="Roller", value=role_text or "Rol bulunamadı", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="emoji", description="Sunucudaki emojileri listeler")
    async def emoji(self, interaction: discord.Interaction):
        guild = interaction.guild
        emojis = guild.emojis
        
        embed = discord.Embed(
            title=f"{guild.name} Emojileri",
            description=f"Toplam {len(emojis)} emoji bulunuyor",
            color=discord.Color.purple()
        )
        
        # Emojileri 10'ar gruplar halinde listele
        emoji_text = ""
        for i, emoji in enumerate(emojis, 1):
            emoji_text += f"{emoji} "
            if i % 10 == 0:
                emoji_text += "\n"
        
        embed.add_field(name="Emojiler", value=emoji_text or "Emoji bulunamadı", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(SunucuKomutlar(bot))
