import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
import database
import os

class RankKomutlar(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name="rank", description="Rank sistemi komutları")
        self.bot = bot
    
    @app_commands.command(name="profil", description="Rank profilinizi veya başka birinin profilini görüntüleyin")
    async def rank(self, interaction: discord.Interaction, kullanıcı: discord.Member = None):
        user = kullanıcı or interaction.user
        guild = interaction.guild
        
        # Kullanıcı rankını al
        rank_data = await database.get_user_rank(user.id, guild.id)
        
        # Bir sonraki level için ilerleme hesapla
        current_xp = rank_data["xp"]
        next_level_xp = rank_data["next_level_xp"]
        prev_level_xp = 0 if rank_data["level"] == 0 else (next_level_xp - 100)  # Basit hesaplama
        
        # İlerleme yüzdesi
        progress = (current_xp - prev_level_xp) / (next_level_xp - prev_level_xp) * 100 if (next_level_xp - prev_level_xp) > 0 else 0
        
        # İlerleme çubuğu oluştur
        progress_bar = ""
        bar_length = 12
        filled_length = round(progress / (100 / bar_length))
        
        for i in range(bar_length):
            progress_bar += "█" if i < filled_length else "░"
        
        # Embed oluştur
        embed = discord.Embed(
            title=f"{user.display_name}'nin Profili",
            color=user.color
        )
        
        embed.set_thumbnail(url=user.display_avatar.url)
        
        embed.add_field(
            name=f"Level {rank_data['level']}",
            value=f"XP: {current_xp}/{next_level_xp}\n{progress_bar} {round(progress)}%",
            inline=False
        )
        
        embed.add_field(
            name="İstatistikler",
            value=f"Sıralama: #{rank_data['rank_position']}\nMesaj Sayısı: {rank_data['messages']}\nToplam XP: {current_xp}",
            inline=False
        )
        
        # Kullanıcının rankına göre rol bilgisini ekle
        roles = await database.get_rank_roles()
        user_rank_role = None
        next_rank_role = None
        
        for level, role_id in roles:
            if level <= rank_data["level"]:
                user_rank_role = role_id
            elif next_rank_role is None:
                next_rank_role = (level, role_id)
                break
        
        if user_rank_role:
            role = guild.get_role(user_rank_role)
            if role:
                embed.add_field(
                    name="Mevcut Rank",
                    value=f"{role.mention}",
                    inline=True
                )
        
        if next_rank_role:
            next_level, next_role_id = next_rank_role
            role = guild.get_role(next_role_id)
            if role:
                xp_needed = (next_level * 100) - current_xp
                embed.add_field(
                    name="Sonraki Rank",
                    value=f"{role.mention} (Level {next_level})\n{xp_needed} XP gerekiyor",
                    inline=True
                )
        
        embed.set_footer(text=f"Son güncelleme: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="liderlik", description="Sunucu liderlik tablosunu göster")
    async def leaderboard(self, interaction: discord.Interaction, limit: int = 10):
        guild = interaction.guild
        
        if limit < 1:
            limit = 10
        elif limit > 25:
            limit = 25  # Maksimum 25 kişi göster
        
        # Liderlik tablosunu al
        leaderboard_data = await database.get_leaderboard(guild.id, limit)
        
        if not leaderboard_data:
            return await interaction.response.send_message(
                "Henüz liderlik tablosunda hiç kimse yok!",
                ephemeral=True
            )
        
        # Embed oluştur
        embed = discord.Embed(
            title=f"{guild.name} Liderlik Tablosu",
            description=f"En yüksek XP'ye sahip {len(leaderboard_data)} kullanıcı",
            color=discord.Color.gold()
        )
        
        # Liderlik tablosunu düzenle
        rank_text = ""
        name_text = ""
        level_text = ""
        
        for index, (user_id, xp, level, messages) in enumerate(leaderboard_data, 1):
            # Madalyalar ekle
            medal = ""
            if index == 1:
                medal = "🥇 "
            elif index == 2:
                medal = "🥈 "
            elif index == 3:
                medal = "🥉 "
                
            member = guild.get_member(user_id)
            name = member.display_name if member else f"Bilinmeyen Kullanıcı ({user_id})"
            
            rank_text += f"**{index}.** {medal}\n"
            name_text += f"{name}\n"
            level_text += f"Level {level} ({xp} XP)\n"
        
        embed.add_field(name="Sıra", value=rank_text, inline=True)
        embed.add_field(name="Kullanıcı", value=name_text, inline=True)
        embed.add_field(name="Seviye", value=level_text, inline=True)
        
        embed.set_footer(text=f"Kendi sıranızı görmek için /rank profil komutunu kullanın")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rol_ayarla", description="Belirli bir seviye için otomatik rol ata")
    @app_commands.describe(
        seviye="Rolün atanacağı seviye",
        rol="Atanacak rol"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_role(self, interaction: discord.Interaction, seviye: int, rol: discord.Role):
        if seviye < 1:
            return await interaction.response.send_message("Seviye 1'den küçük olamaz!", ephemeral=True)
        
        # Rolü ayarla
        await database.set_rank_role(seviye, rol.id)
        
        await interaction.response.send_message(
            f"Level {seviye} için rank rolü {rol.mention} olarak ayarlandı.",
            ephemeral=True
        )
    
    @app_commands.command(name="roller", description="Tüm rank rollerini görüntüle")
    async def view_roles(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        # Tüm rol ayarlarını al
        roles = await database.get_rank_roles()
        
        if not roles:
            return await interaction.response.send_message(
                "Henüz hiç rank rolü ayarlanmamış!",
                ephemeral=True
            )
        
        # Embed oluştur
        embed = discord.Embed(
            title="Rank Rolleri",
            description="Aşağıdaki seviyeler için otomatik roller atanacaktır:",
            color=discord.Color.blue()
        )
        
        for level, role_id in roles:
            role = guild.get_role(role_id)
            if role:
                embed.add_field(
                    name=f"Level {level}",
                    value=role.mention,
                    inline=True
                )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="kurulum", description="Rank sistemini otomatik olarak kur")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_ranks(self, interaction: discord.Interaction):
        """Belirtilen rolleri otomatik olarak ayarla"""
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        
        # Rolleri txt dosyasından oku
        rank_roles = {}
        roles_txt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rank_roles.txt')
        
        try:
            with open(roles_txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # # ile başlayan satırları yorum olarak atla
                    if not line or line.startswith('#'):
                        continue
                    
                    # level=role_id formatında olmalı
                    if '=' in line:
                        parts = line.split('=')
                        if len(parts) == 2:
                            try:
                                level = int(parts[0].strip())
                                role_id = int(parts[1].strip())
                                rank_roles[level] = role_id
                            except ValueError:
                                continue
        except Exception as e:
            await interaction.followup.send(f"Rol dosyası okunurken bir hata oluştu: {e}")
            return
        
        if not rank_roles:
            await interaction.followup.send("Rol dosyasında geçerli rol tanımı bulunamadı. Lütfen rank_roles.txt dosyasını kontrol edin.")
            return
        
        # Rolleri ayarla
        set_roles = []
        for level, role_id in rank_roles.items():
            role = guild.get_role(role_id)
            if role:
                await database.set_rank_role(level, role_id)
                set_roles.append(f"• Level {level}: {role.name}")
        
        if set_roles:
            await interaction.followup.send(
                f"Rank rolleri başarıyla ayarlandı:\n" + "\n".join(set_roles)
            )
        else:
            await interaction.followup.send("Hiçbir rol ayarlanamadı. Rol ID'lerinin doğru olduğundan emin olun.")

async def setup(bot):
    # Veritabanını başlat
    await database.init_db()
    bot.tree.add_command(RankKomutlar(bot))
    
    # XP event listener ekle
    @bot.event
    async def on_message(message):
        # Botları ve DM'leri görmezden gel
        if message.author.bot or not message.guild:
            return
        
        # Komut çağrılarını işlemeye devam et
        if isinstance(bot, commands.Bot):
            await bot.process_commands(message)
        
        # XP ayarlarını al
        settings = await database.get_xp_settings(message.guild.id)
        xp_amount = settings["xp_per_message"]
        cooldown = settings["xp_cooldown"]
        
        # Kullanıcının son mesaj zamanını kontrol et
        last_message_time = await database.get_cooldown(message.author.id, message.guild.id)
        if last_message_time:
            # String timestamp'i datetime'a çevir
            try:
                last_time = datetime.datetime.fromisoformat(last_message_time.replace('Z', '+00:00'))
                now = datetime.datetime.now(datetime.timezone.utc)
                
                # Cooldown kontrolü
                seconds_diff = (now - last_time.replace(tzinfo=datetime.timezone.utc)).total_seconds()
                if seconds_diff < cooldown:
                    return  # Cooldown süresi dolmadı
            except (ValueError, TypeError):
                pass  # Hata durumunda devam et
        
        # XP ekle
        result = await database.add_xp(message.author.id, message.guild.id, xp_amount)
        
        # Level atladıysa rol ver (sessiz bir şekilde, bildirim olmadan)
        if result["level_up"] and result["role_id"]:
            role = message.guild.get_role(result["role_id"])
            if role and not role in message.author.roles:
                try:
                    await message.author.add_roles(role)
                except discord.Forbidden:
                    pass  # Rol verme yetkisi yok
