import discord
from discord import app_commands
from discord.ext import commands

class ModerasyonKomutlar(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name="moderasyon", description="Moderasyon komutları")
        self.bot = bot
    
    @app_commands.command(name="temizle", description="Belirtilen sayıda mesajı siler")
    @app_commands.describe(sayı="Silinecek mesaj sayısı (1-100 arası)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def temizle(self, interaction: discord.Interaction, sayı: int):
        if sayı < 1 or sayı > 100:
            return await interaction.response.send_message("Lütfen 1 ile 100 arasında bir sayı belirtin.", ephemeral=True)
        
        # Etkileşime yanıt verelim
        await interaction.response.defer(ephemeral=True)
        
        # Mesajları silelim
        channel = interaction.channel
        deleted = await channel.purge(limit=sayı)
        
        await interaction.followup.send(f"{len(deleted)} mesaj silindi.", ephemeral=True)
    
    @temizle.error
    async def temizle_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Bu komutu kullanmak için 'Mesajları Yönet' yetkisine sahip olmanız gerekiyor.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Bir hata oluştu: {error}", ephemeral=True)
    
    @app_commands.command(name="at", description="Bir kullanıcıyı sunucudan atar")
    @app_commands.describe(kullanıcı="Atılacak kullanıcı", sebep="Atılma sebebi (isteğe bağlı)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def at(self, interaction: discord.Interaction, kullanıcı: discord.Member, sebep: str = None):
        # Botun ve komut kullanan kişinin yetkisi kontrol edilir
        if kullanıcı.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message("Bu kullanıcıyı atamazsınız çünkü sizden daha yüksek veya eşit bir role sahip.", ephemeral=True)
        
        if kullanıcı.top_role >= interaction.guild.me.top_role:
            return await interaction.response.send_message("Bu kullanıcıyı atamam çünkü benden daha yüksek veya eşit bir role sahip.", ephemeral=True)
        
        try:
            await kullanıcı.kick(reason=f"{interaction.user} tarafından atıldı. Sebep: {sebep or 'Belirtilmedi'}")
            
            # Başarılı mesajı
            embed = discord.Embed(
                title="Kullanıcı Atıldı",
                description=f"{kullanıcı.mention} ({kullanıcı.name}) sunucudan atıldı.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Sebep", value=sebep or "Belirtilmedi")
            embed.add_field(name="Moderatör", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("Bu kullanıcıyı atmak için yeterli yetkiye sahip değilim.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Bir hata oluştu: {e}", ephemeral=True)
    
    @at.error
    async def at_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Bu komutu kullanmak için 'Üyeleri At' yetkisine sahip olmanız gerekiyor.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Bir hata oluştu: {error}", ephemeral=True)
    
    @app_commands.command(name="yasakla", description="Bir kullanıcıyı sunucudan yasaklar")
    @app_commands.describe(kullanıcı="Yasaklanacak kullanıcı", sebep="Yasaklama sebebi (isteğe bağlı)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def yasakla(self, interaction: discord.Interaction, kullanıcı: discord.Member, sebep: str = None):
        # Botun ve komut kullanan kişinin yetkisi kontrol edilir
        if kullanıcı.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message("Bu kullanıcıyı yasaklayamazsınız çünkü sizden daha yüksek veya eşit bir role sahip.", ephemeral=True)
        
        if kullanıcı.top_role >= interaction.guild.me.top_role:
            return await interaction.response.send_message("Bu kullanıcıyı yasaklayamam çünkü benden daha yüksek veya eşit bir role sahip.", ephemeral=True)
        
        try:
            await kullanıcı.ban(reason=f"{interaction.user} tarafından yasaklandı. Sebep: {sebep or 'Belirtilmedi'}")
            
            # Başarılı mesajı
            embed = discord.Embed(
                title="Kullanıcı Yasaklandı",
                description=f"{kullanıcı.mention} ({kullanıcı.name}) sunucudan yasaklandı.",
                color=discord.Color.red()
            )
            embed.add_field(name="Sebep", value=sebep or "Belirtilmedi")
            embed.add_field(name="Moderatör", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("Bu kullanıcıyı yasaklamak için yeterli yetkiye sahip değilim.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Bir hata oluştu: {e}", ephemeral=True)
    
    @yasakla.error
    async def yasakla_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Bu komutu kullanmak için 'Üyeleri Yasakla' yetkisine sahip olmanız gerekiyor.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Bir hata oluştu: {error}", ephemeral=True)
    
    @app_commands.command(name="yasak_kaldır", description="Bir kullanıcının yasağını kaldırır")
    @app_commands.describe(kullanıcı_id="Yasağı kaldırılacak kullanıcının ID'si", sebep="Yasak kaldırma sebebi (isteğe bağlı)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def yasak_kaldir(self, interaction: discord.Interaction, kullanıcı_id: str, sebep: str = None):
        try:
            # Kullanıcı ID'si kontrol edilir
            user_id = int(kullanıcı_id)
            guild = interaction.guild
            
            # Yasağı kaldır
            await guild.unban(discord.Object(id=user_id), reason=f"{interaction.user} tarafından yasak kaldırıldı. Sebep: {sebep or 'Belirtilmedi'}")
            
            # Başarılı mesajı
            embed = discord.Embed(
                title="Yasak Kaldırıldı",
                description=f"<@{user_id}> kullanıcısının yasağı kaldırıldı.",
                color=discord.Color.green()
            )
            embed.add_field(name="Sebep", value=sebep or "Belirtilmedi")
            embed.add_field(name="Moderatör", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message("Geçerli bir kullanıcı ID'si giriniz.", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("Bu ID'ye sahip yasaklı bir kullanıcı bulunamadı.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Kullanıcının yasağını kaldırmak için yeterli yetkiye sahip değilim.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Bir hata oluştu: {e}", ephemeral=True)
    
    @yasak_kaldir.error
    async def yasak_kaldir_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Bu komutu kullanmak için 'Üyeleri Yasakla' yetkisine sahip olmanız gerekiyor.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Bir hata oluştu: {error}", ephemeral=True)
    
    @app_commands.command(name="söyle", description="Bot aracılığıyla belirtilen kanala mesaj gönder")
    @app_commands.describe(
        kanal="Mesajın gönderileceği kanal",
        mesaj="Gönderilecek mesaj",
        embed="Mesajın gömülü (embed) olarak gönderilip gönderilmeyeceği (varsayılan: False)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def soyle(self, interaction: discord.Interaction, kanal: discord.TextChannel, mesaj: str, embed: bool = False):
        try:
            # Mesajı gönder
            if embed:
                # Embed olarak gönder
                embed_mesaj = discord.Embed(
                    description=mesaj,
                    color=discord.Color.blue()
                )
                embed_mesaj.set_footer(text=f"Gönderen: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
                await kanal.send(embed=embed_mesaj)
            else:
                # Normal mesaj olarak gönder
                await kanal.send(mesaj)
                
            # Başarılı mesajı
            await interaction.response.send_message(f"Mesaj başarıyla {kanal.mention} kanalına gönderildi.", ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(f"Bu kanala mesaj gönderme yetkim yok: {kanal.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Mesaj gönderilirken bir hata oluştu: {e}", ephemeral=True)
    
    @soyle.error
    async def soyle_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("Bu komutu kullanmak için 'Yönetici' yetkisine sahip olmanız gerekiyor.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Bir hata oluştu: {error}", ephemeral=True)

async def setup(bot):
    bot.tree.add_command(ModerasyonKomutlar(bot))
