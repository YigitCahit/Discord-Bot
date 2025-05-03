import os
import aiosqlite
import asyncio

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bot_data.db')

async def init_db():
    """Veritabanını oluştur ve tabloları ayarla"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Rank tablosunu oluştur
        await db.execute('''
        CREATE TABLE IF NOT EXISTS user_ranks (
            user_id INTEGER PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 0,
            messages INTEGER DEFAULT 0,
            last_message_time TEXT,
            UNIQUE(user_id, guild_id)
        )
        ''')
        
        # Level tablosunu oluştur (level başına gereken XP)
        await db.execute('''
        CREATE TABLE IF NOT EXISTS level_settings (
            level INTEGER PRIMARY KEY,
            xp_required INTEGER NOT NULL
        )
        ''')
        
        # Rol tablosunu oluştur (level başına verilecek roller)
        await db.execute('''
        CREATE TABLE IF NOT EXISTS rank_roles (
            level INTEGER PRIMARY KEY,
            role_id INTEGER NOT NULL
        )
        ''')
        
        # Ayarlar tablosunu oluştur
        await db.execute('''
        CREATE TABLE IF NOT EXISTS rank_settings (
            guild_id INTEGER PRIMARY KEY,
            xp_per_message INTEGER DEFAULT 5,
            xp_cooldown INTEGER DEFAULT 60,
            level_up_channel INTEGER DEFAULT NULL
        )
        ''')
        
        await db.commit()
        
        # Temel level gereksinimlerini kur (eğer yoksa)
        cursor = await db.execute('SELECT COUNT(*) FROM level_settings')
        count = await cursor.fetchone()
        if count[0] == 0:
            # Basit bir level sistemi: her level için (level * 100) XP gerekir
            for level in range(1, 101):  # 1-100 arası level
                await db.execute('INSERT INTO level_settings VALUES (?, ?)', 
                               (level, level * 100))
            await db.commit()

async def add_xp(user_id, guild_id, xp_amount):
    """Kullanıcıya XP ekle ve level atladıysa bilgi döndür"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Kullanıcıyı al veya oluştur
        await db.execute('''
        INSERT OR IGNORE INTO user_ranks (user_id, guild_id, xp, level, messages)
        VALUES (?, ?, 0, 0, 0)
        ''', (user_id, guild_id))
        
        # XP ekle
        await db.execute('''
        UPDATE user_ranks 
        SET xp = xp + ?, messages = messages + 1, last_message_time = CURRENT_TIMESTAMP
        WHERE user_id = ? AND guild_id = ?
        ''', (xp_amount, user_id, guild_id))
        
        # Kullanıcının güncel XP ve levelini al
        cursor = await db.execute('''
        SELECT xp, level FROM user_ranks
        WHERE user_id = ? AND guild_id = ?
        ''', (user_id, guild_id))
        user_data = await cursor.fetchone()
        current_xp, current_level = user_data
        
        # Bir sonraki level için gereken XP'yi al
        cursor = await db.execute('''
        SELECT xp_required FROM level_settings
        WHERE level = ?
        ''', (current_level + 1,))
        next_level_data = await cursor.fetchone()
        
        level_up = False
        new_level = current_level
        
        # Level atlama kontrolü
        if next_level_data and current_xp >= next_level_data[0]:
            new_level = current_level + 1
            level_up = True
            await db.execute('''
            UPDATE user_ranks 
            SET level = ?
            WHERE user_id = ? AND guild_id = ?
            ''', (new_level, user_id, guild_id))
        
        await db.commit()
        
        # Level atladıysa sonraki level için gereken rolü al
        role_id = None
        if level_up:
            cursor = await db.execute('''
            SELECT role_id FROM rank_roles
            WHERE level = ?
            ''', (new_level,))
            role_data = await cursor.fetchone()
            if role_data:
                role_id = role_data[0]
        
        return {
            "level_up": level_up,
            "new_level": new_level,
            "current_xp": current_xp,
            "role_id": role_id
        }

async def get_user_rank(user_id, guild_id):
    """Kullanıcının rank bilgilerini al"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Kullanıcı varsa bilgilerini al
        cursor = await db.execute('''
        SELECT xp, level, messages FROM user_ranks
        WHERE user_id = ? AND guild_id = ?
        ''', (user_id, guild_id))
        user_data = await cursor.fetchone()
        
        if not user_data:
            return {
                "xp": 0,
                "level": 0,
                "messages": 0,
                "next_level_xp": 100,
                "rank_position": 0
            }
        
        current_xp, current_level, messages = user_data
        
        # Bir sonraki level için gereken XP'yi al
        cursor = await db.execute('''
        SELECT xp_required FROM level_settings
        WHERE level = ?
        ''', (current_level + 1,))
        next_level_data = await cursor.fetchone()
        next_level_xp = next_level_data[0] if next_level_data else current_xp + 100
        
        # Kullanıcının sıralamasını bul
        cursor = await db.execute('''
        SELECT COUNT(*) + 1 FROM user_ranks
        WHERE (guild_id = ? AND xp > (SELECT xp FROM user_ranks WHERE user_id = ? AND guild_id = ?))
        ''', (guild_id, user_id, guild_id))
        rank_position = await cursor.fetchone()
        
        return {
            "xp": current_xp,
            "level": current_level,
            "messages": messages,
            "next_level_xp": next_level_xp,
            "rank_position": rank_position[0] if rank_position else 0
        }

async def get_leaderboard(guild_id, limit=10):
    """Sunucu sıralamasını al"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute('''
        SELECT user_id, xp, level, messages FROM user_ranks
        WHERE guild_id = ?
        ORDER BY xp DESC
        LIMIT ?
        ''', (guild_id, limit))
        leaderboard = await cursor.fetchall()
        return leaderboard

async def set_rank_role(level, role_id):
    """Bir level için otomatik verilecek rolü ayarla"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
        INSERT OR REPLACE INTO rank_roles (level, role_id)
        VALUES (?, ?)
        ''', (level, role_id))
        await db.commit()

async def get_rank_roles():
    """Tüm rank rollerini al"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute('SELECT level, role_id FROM rank_roles ORDER BY level')
        roles = await cursor.fetchall()
        return roles

async def get_cooldown(user_id, guild_id):
    """Kullanıcının son mesaj zamanını kontrol et"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute('''
        SELECT last_message_time FROM user_ranks
        WHERE user_id = ? AND guild_id = ?
        ''', (user_id, guild_id))
        time_data = await cursor.fetchone()
        return time_data[0] if time_data else None

async def get_xp_settings(guild_id):
    """XP ayarlarını al"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Sunucu için XP ayarlarını kontrol et, yoksa oluştur
        await db.execute('''
        INSERT OR IGNORE INTO rank_settings (guild_id)
        VALUES (?)
        ''', (guild_id,))
        await db.commit()
        
        # Ayarları al
        cursor = await db.execute('''
        SELECT xp_per_message, xp_cooldown, level_up_channel FROM rank_settings
        WHERE guild_id = ?
        ''', (guild_id,))
        settings = await cursor.fetchone()
        
        if settings:
            return {
                "xp_per_message": settings[0],
                "xp_cooldown": settings[1],
                "level_up_channel": settings[2]
            }
        return {
            "xp_per_message": 5,
            "xp_cooldown": 60,
            "level_up_channel": None
        }
