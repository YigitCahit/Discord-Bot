import discord
from discord import app_commands

class KullaniciKomutlar(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name="kullanıcı", description="Kullanıcı ile ilgili komutlar")
        self.bot = bot
    
    @app_commands.command(name="avatar", description="Kullanıcının avatarını göster")
    async def avatar(self, interaction: discord.Interaction, kullanıcı: discord.Member = None):
        kullanıcı = kullanıcı or interaction.user
        
        embed = discord.Embed(
            title=f"{kullanıcı.name} Avatarı",
            color=discord.Color.purple()
        )
        embed.set_image(url=kullanıcı.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="bilgi", description="Kullanıcı hakkında bilgi göster")
    async def bilgi(self, interaction: discord.Interaction, kullanıcı: discord.Member = None):
        kullanıcı = kullanıcı or interaction.user
        
        # Kullanıcının hesap oluşturma tarihi ve sunucuya katılma tarihi
        created_at = kullanıcı.created_at.strftime("%d/%m/%Y")
        joined_at = kullanıcı.joined_at.strftime("%d/%m/%Y") if kullanıcı.joined_at else "Bilinmiyor"
        
        # Kullanıcının rolleri
        roles = [role.mention for role in kullanıcı.roles[1:]]  # @everyone rolünü hariç tut
        roles_str = ", ".join(roles) if roles else "Rol yok"
        
        embed = discord.Embed(
            title=f"{kullanıcı.name} Bilgisi",
            description=f"ID: {kullanıcı.id}",
            color=kullanıcı.color
        )
        
        embed.set_thumbnail(url=kullanıcı.display_avatar.url)
        embed.add_field(name="Takma Ad", value=kullanıcı.display_name, inline=True)
        embed.add_field(name="Hesap Oluşturulma", value=created_at, inline=True)
        embed.add_field(name="Sunucuya Katılma", value=joined_at, inline=True)
        
        # Roller alanı çok uzun olabileceği için ayrı bir alan olarak ekle
        embed.add_field(name=f"Roller [{len(roles)}]", value=roles_str, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="sunucular", description="Botun bulunduğu ortak sunucuları göster")
    async def sunucular(self, interaction: discord.Interaction, kullanıcı: discord.Member = None):
        kullanıcı = kullanıcı or interaction.user
        
        # Botun da bulunduğu kullanıcının sunucuları listelenemez, bu bir Discord API kısıtlamasıdır
        # Bu nedenle sadece bilgilendirme mesajı gönderiyoruz
        await interaction.response.send_message(
            "Discord API kısıtlamaları nedeniyle, bir kullanıcının hangi sunucularda olduğu bilgisine erişemiyorum. "
            "Bu bilgi yalnızca Discord'un kendi sisteminde görülebilir.",
            ephemeral=True
        )

async def setup(bot):
    bot.tree.add_command(KullaniciKomutlar(bot))
