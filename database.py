# database.py - مدیریت دیتابیس

import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH, DEFAULT_SETTINGS

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """ایجاد جداول دیتابیس"""
        
        # جدول گروه‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                title TEXT,
                username TEXT,
                settings TEXT,
                rules TEXT,
                welcome_message TEXT,
                goodbye_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                added_by INTEGER,
                language TEXT DEFAULT 'fa'
            )
        ''')
        
        # جدول کاربران
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'fa',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_banned INTEGER DEFAULT 0,
                ban_reason TEXT,
                total_messages INTEGER DEFAULT 0,
                total_points INTEGER DEFAULT 0
            )
        ''')
        
        # جدول اعضای گروه
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                messages INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                warns INTEGER DEFAULT 0,
                warn_reasons TEXT,
                is_muted INTEGER DEFAULT 0,
                mute_until TIMESTAMP,
                is_banned INTEGER DEFAULT 0,
                ban_reason TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_message_at TIMESTAMP,
                captcha_verified INTEGER DEFAULT 0,
                UNIQUE(chat_id, user_id)
            )
        ''')
        
        # جدول ادمین‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                permissions TEXT,
                promoted_by INTEGER,
                promoted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, user_id)
            )
        ''')
        
        # جدول فیلترها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                trigger_word TEXT,
                response TEXT,
                response_type TEXT DEFAULT 'text',
                file_id TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول یادآوری‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                message TEXT,
                remind_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_sent INTEGER DEFAULT 0
            )
        ''')
        
        # جدول نظرسنجی‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                question TEXT,
                options TEXT,
                votes TEXT,
                is_anonymous INTEGER DEFAULT 1,
                is_multiple INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ends_at TIMESTAMP
            )
        ''')
        
        # جدول بازی‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                game_type TEXT,
                game_data TEXT,
                is_active INTEGER DEFAULT 1,
                started_by INTEGER,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                winner_id INTEGER
            )
        ''')
        
        # جدول امتیازات بازی
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                game_type TEXT,
                score INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                UNIQUE(chat_id, user_id, game_type)
            )
        ''')
        
        # جدول نوت‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                note_name TEXT,
                note_content TEXT,
                note_type TEXT DEFAULT 'text',
                file_id TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, note_name)
            )
        ''')
        
        # جدول لاگ‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول بک‌آپ تنظیمات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                backup_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول گزارش‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                reporter_id INTEGER,
                reported_user_id INTEGER,
                message_id INTEGER,
                reason TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                resolved_by INTEGER
            )
        ''')
        
        # جدول AFK
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS afk_users (
                user_id INTEGER PRIMARY KEY,
                reason TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول سکه‌ها و اقتصاد
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS economy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                coins INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0,
                daily_claimed TIMESTAMP,
                weekly_claimed TIMESTAMP,
                work_cooldown TIMESTAMP,
                UNIQUE(chat_id, user_id)
            )
        ''')
        
        # جدول فروشگاه
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shop_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                item_name TEXT,
                item_type TEXT,
                price INTEGER,
                description TEXT,
                stock INTEGER DEFAULT -1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول خریدهای کاربران
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                item_id INTEGER,
                quantity INTEGER DEFAULT 1,
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول تگ‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                tag_name TEXT,
                user_ids TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, tag_name)
            )
        ''')
        
        # جدول زمان‌بندی پیام‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                message TEXT,
                message_type TEXT DEFAULT 'text',
                file_id TEXT,
                scheduled_at TIMESTAMP,
                repeat_type TEXT,
                is_sent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول لینک‌های سفید
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS whitelisted_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                link TEXT,
                added_by INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول کلمات ممنوعه
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS banned_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                word TEXT,
                action TEXT DEFAULT 'delete',
                added_by INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول قرعه‌کشی‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS giveaways (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                prize TEXT,
                winners_count INTEGER DEFAULT 1,
                participants TEXT,
                ends_at TIMESTAMP,
                winners TEXT,
                is_active INTEGER DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول تیکت‌ها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                subject TEXT,
                message TEXT,
                status TEXT DEFAULT 'open',
                priority TEXT DEFAULT 'normal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                closed_by INTEGER
            )
        ''')
        
        # جدول پاسخ‌های تیکت
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticket_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER,
                user_id INTEGER,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول رویدادها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                title TEXT,
                description TEXT,
                event_date TIMESTAMP,
                participants TEXT,
                max_participants INTEGER,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول سودوها
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sudos (
                user_id INTEGER PRIMARY KEY,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول گروه‌های مجاز
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS allowed_groups (
                chat_id INTEGER PRIMARY KEY,
                added_by INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    # ==================== توابع گروه ====================
    
    def add_group(self, chat_id, title, username=None, added_by=None):
        """اضافه کردن گروه جدید"""
        settings = json.dumps(DEFAULT_SETTINGS)
        self.cursor.execute('''
            INSERT OR REPLACE INTO groups 
            (chat_id, title, username, settings, added_by, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (chat_id, title, username, settings, added_by, datetime.now()))
        self.conn.commit()
    
    def get_group(self, chat_id):
        """دریافت اطلاعات گروه"""
        self.cursor.execute('SELECT * FROM groups WHERE chat_id = ?', (chat_id,))
        return self.cursor.fetchone()
    
    def get_group_settings(self, chat_id):
        """دریافت تنظیمات گروه"""
        self.cursor.execute('SELECT settings FROM groups WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        return DEFAULT_SETTINGS.copy()
    
    def update_group_settings(self, chat_id, settings):
        """بروزرسانی تنظیمات گروه"""
        self.cursor.execute('''
            UPDATE groups SET settings = ?, updated_at = ?
            WHERE chat_id = ?
        ''', (json.dumps(settings), datetime.now(), chat_id))
        self.conn.commit()
    
    def set_group_rules(self, chat_id, rules):
        """تنظیم قوانین گروه"""
        self.cursor.execute('''
            UPDATE groups SET rules = ?, updated_at = ?
            WHERE chat_id = ?
        ''', (rules, datetime.now(), chat_id))
        self.conn.commit()
    
    def get_group_rules(self, chat_id):
        """دریافت قوانین گروه"""
        self.cursor.execute('SELECT rules FROM groups WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def set_welcome_message(self, chat_id, message):
        """تنظیم پیام خوش‌آمدگویی"""
        self.cursor.execute('''
            UPDATE groups SET welcome_message = ?, updated_at = ?
            WHERE chat_id = ?
        ''', (message, datetime.now(), chat_id))
        self.conn.commit()
    
    def get_welcome_message(self, chat_id):
        """دریافت پیام خوش‌آمدگویی"""
        self.cursor.execute('SELECT welcome_message FROM groups WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def set_goodbye_message(self, chat_id, message):
        """تنظیم پیام خداحافظی"""
        self.cursor.execute('''
            UPDATE groups SET goodbye_message = ?, updated_at = ?
            WHERE chat_id = ?
        ''', (message, datetime.now(), chat_id))
        self.conn.commit()
    
    def get_goodbye_message(self, chat_id):
        """دریافت پیام خداحافظی"""
        self.cursor.execute('SELECT goodbye_message FROM groups WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def remove_group(self, chat_id):
        """حذف گروه"""
        self.cursor.execute('DELETE FROM groups WHERE chat_id = ?', (chat_id,))
        self.conn.commit()
    
    def get_all_groups(self):
        """دریافت همه گروه‌ها"""
        self.cursor.execute('SELECT * FROM groups WHERE is_active = 1')
        return self.cursor.fetchall()
    
    def get_groups_count(self):
        """دریافت تعداد گروه‌ها"""
        self.cursor.execute('SELECT COUNT(*) FROM groups WHERE is_active = 1')
        return self.cursor.fetchone()[0]
    
    # ==================== توابع کاربر ====================
    
    def add_user(self, user_id, username=None, first_name=None, last_name=None):
        """اضافه کردن کاربر"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        self.conn.commit()
    
    def get_user(self, user_id):
        """دریافت اطلاعات کاربر"""
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    
    def update_user(self, user_id, **kwargs):
        """بروزرسانی اطلاعات کاربر"""
        fields = ', '.join([f'{k} = ?' for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        self.cursor.execute(f'UPDATE users SET {fields} WHERE user_id = ?', values)
        self.conn.commit()
    
    def get_all_users(self):
        """دریافت همه کاربران"""
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def get_users_count(self):
        """دریافت تعداد کاربران"""
        self.cursor.execute('SELECT COUNT(*) FROM users')
        return self.cursor.fetchone()[0]
    
    # ==================== توابع اعضای گروه ====================
    
    def add_group_member(self, chat_id, user_id):
        """اضافه کردن عضو به گروه"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO group_members 
            (chat_id, user_id)
            VALUES (?, ?)
        ''', (chat_id, user_id))
        self.conn.commit()
    
    def get_group_member(self, chat_id, user_id):
        """دریافت اطلاعات عضو گروه"""
        self.cursor.execute('''
            SELECT * FROM group_members 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        return self.cursor.fetchone()
    
    def update_member_messages(self, chat_id, user_id, increment=1):
        """بروزرسانی تعداد پیام‌های عضو"""
        self.cursor.execute('''
            UPDATE group_members 
            SET messages = messages + ?, last_message_at = ?
            WHERE chat_id = ? AND user_id = ?
        ''', (increment, datetime.now(), chat_id, user_id))
        self.conn.commit()
    
    def update_member_points(self, chat_id, user_id, points):
        """بروزرسانی امتیاز عضو"""
        self.cursor.execute('''
            UPDATE group_members 
            SET points = points + ?
            WHERE chat_id = ? AND user_id = ?
        ''', (points, chat_id, user_id))
        self.conn.commit()
    
    def get_member_stats(self, chat_id, user_id):
        """دریافت آمار عضو"""
        self.cursor.execute('''
            SELECT messages, points, warns FROM group_members 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        return self.cursor.fetchone()
    
    def get_group_leaderboard(self, chat_id, limit=10):
        """دریافت برترین‌های گروه"""
        self.cursor.execute('''
            SELECT user_id, messages, points FROM group_members 
            WHERE chat_id = ?
            ORDER BY messages DESC
            LIMIT ?
        ''', (chat_id, limit))
        return self.cursor.fetchall()
    
    def get_group_members_count(self, chat_id):
        """دریافت تعداد اعضای گروه"""
        self.cursor.execute('''
            SELECT COUNT(*) FROM group_members WHERE chat_id = ?
        ''', (chat_id,))
        return self.cursor.fetchone()[0]
    
    # ==================== توابع اخطار ====================
    
    def add_warn(self, chat_id, user_id, reason=None):
        """اضافه کردن اخطار"""
        member = self.get_group_member(chat_id, user_id)
        if member:
            warns = member[5] + 1  # index of warns column
            warn_reasons = json.loads(member[6]) if member[6] else []
            warn_reasons.append({
                'reason': reason,
                'time': datetime.now().isoformat()
            })
            self.cursor.execute('''
                UPDATE group_members 
                SET warns = ?, warn_reasons = ?
                WHERE chat_id = ? AND user_id = ?
            ''', (warns, json.dumps(warn_reasons), chat_id, user_id))
            self.conn.commit()
            return warns
        return 0
    
    def remove_warn(self, chat_id, user_id, count=1):
        """حذف اخطار"""
        self.cursor.execute('''
            UPDATE group_members 
            SET warns = MAX(0, warns - ?)
            WHERE chat_id = ? AND user_id = ?
        ''', (count, chat_id, user_id))
        self.conn.commit()
    
    def reset_warns(self, chat_id, user_id):
        """ریست کردن اخطارها"""
        self.cursor.execute('''
            UPDATE group_members 
            SET warns = 0, warn_reasons = NULL
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        self.conn.commit()
    
    def get_warns(self, chat_id, user_id):
        """دریافت تعداد اخطارها"""
        self.cursor.execute('''
            SELECT warns, warn_reasons FROM group_members 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        result = self.cursor.fetchone()
        if result:
            return result[0], json.loads(result[1]) if result[1] else []
        return 0, []
    
    # ==================== توابع میوت ====================
    
    def mute_user(self, chat_id, user_id, until=None):
        """سکوت کردن کاربر"""
        self.cursor.execute('''
            UPDATE group_members 
            SET is_muted = 1, mute_until = ?
            WHERE chat_id = ? AND user_id = ?
        ''', (until, chat_id, user_id))
        self.conn.commit()
    
    def unmute_user(self, chat_id, user_id):
        """رفع سکوت کاربر"""
        self.cursor.execute('''
            UPDATE group_members 
            SET is_muted = 0, mute_until = NULL
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        self.conn.commit()
    
    def is_muted(self, chat_id, user_id):
        """بررسی سکوت بودن کاربر"""
        self.cursor.execute('''
            SELECT is_muted, mute_until FROM group_members 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        result = self.cursor.fetchone()
        if result:
            return result[0] == 1
        return False
    
    # ==================== توابع بن ====================
    
    def ban_user(self, chat_id, user_id, reason=None):
        """بن کردن کاربر"""
        self.cursor.execute('''
            UPDATE group_members 
            SET is_banned = 1, ban_reason = ?
            WHERE chat_id = ? AND user_id = ?
        ''', (reason, chat_id, user_id))
        self.conn.commit()
    
    def unban_user(self, chat_id, user_id):
        """آنبن کردن کاربر"""
        self.cursor.execute('''
            UPDATE group_members 
            SET is_banned = 0, ban_reason = NULL
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        self.conn.commit()
    
    def is_banned(self, chat_id, user_id):
        """بررسی بن بودن کاربر"""
        self.cursor.execute('''
            SELECT is_banned FROM group_members 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        result = self.cursor.fetchone()
        if result:
            return result[0] == 1
        return False
    
    # ==================== توابع کپچا ====================
    
    def set_captcha_verified(self, chat_id, user_id, verified=True):
        """تنظیم وضعیت تأیید کپچا"""
        self.cursor.execute('''
            UPDATE group_members 
            SET captcha_verified = ?
            WHERE chat_id = ? AND user_id = ?
        ''', (1 if verified else 0, chat_id, user_id))
        self.conn.commit()
    
    def is_captcha_verified(self, chat_id, user_id):
        """بررسی تأیید کپچا"""
        self.cursor.execute('''
            SELECT captcha_verified FROM group_members 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        result = self.cursor.fetchone()
        if result:
            return result[0] == 1
        return False
    
    # ==================== توابع فیلتر ====================
    
    def add_filter(self, chat_id, trigger, response, response_type='text', file_id=None, created_by=None):
        """اضافه کردن فیلتر"""
        self.cursor.execute('''
            INSERT INTO filters 
            (chat_id, trigger_word, response, response_type, file_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (chat_id, trigger.lower(), response, response_type, file_id, created_by))
        self.conn.commit()
    
    def get_filter(self, chat_id, trigger):
        """دریافت فیلتر"""
        self.cursor.execute('''
            SELECT * FROM filters 
            WHERE chat_id = ? AND trigger_word = ?
        ''', (chat_id, trigger.lower()))
        return self.cursor.fetchone()
    
    def get_all_filters(self, chat_id):
        """دریافت همه فیلترها"""
        self.cursor.execute('''
            SELECT * FROM filters WHERE chat_id = ?
        ''', (chat_id,))
        return self.cursor.fetchall()
    
    def remove_filter(self, chat_id, trigger):
        """حذف فیلتر"""
        self.cursor.execute('''
            DELETE FROM filters 
            WHERE chat_id = ? AND trigger_word = ?
        ''', (chat_id, trigger.lower()))
        self.conn.commit()
    
    def remove_all_filters(self, chat_id):
        """حذف همه فیلترها"""
        self.cursor.execute('DELETE FROM filters WHERE chat_id = ?', (chat_id,))
        self.conn.commit()
    
    # ==================== توابع نوت ====================
    
    def add_note(self, chat_id, name, content, note_type='text', file_id=None, created_by=None):
        """اضافه کردن نوت"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO notes 
            (chat_id, note_name, note_content, note_type, file_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (chat_id, name.lower(), content, note_type, file_id, created_by))
        self.conn.commit()
    
    def get_note(self, chat_id, name):
        """دریافت نوت"""
        self.cursor.execute('''
            SELECT * FROM notes 
            WHERE chat_id = ? AND note_name = ?
        ''', (chat_id, name.lower()))
        return self.cursor.fetchone()
    
    def get_all_notes(self, chat_id):
        """دریافت همه نوت‌ها"""
        self.cursor.execute('SELECT * FROM notes WHERE chat_id = ?', (chat_id,))
        return self.cursor.fetchall()
    
    def remove_note(self, chat_id, name):
        """حذف نوت"""
        self.cursor.execute('''
            DELETE FROM notes 
            WHERE chat_id = ? AND note_name = ?
        ''', (chat_id, name.lower()))
        self.conn.commit()
    
    def remove_all_notes(self, chat_id):
        """حذف همه نوت‌ها"""
        self.cursor.execute('DELETE FROM notes WHERE chat_id = ?', (chat_id,))
        self.conn.commit()
    
    # ==================== توابع اقتصاد ====================
    
    def get_economy(self, chat_id, user_id):
        """دریافت اطلاعات اقتصادی کاربر"""
        self.cursor.execute('''
            SELECT * FROM economy 
            WHERE chat_id = ? AND user_id = ?
        ''', (chat_id, user_id))
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute('''
                INSERT INTO economy (chat_id, user_id)
                VALUES (?, ?)
            ''', (chat_id, user_id))
            self.conn.commit()
            return self.get_economy(chat_id, user_id)
        return result
    
    def update_coins(self, chat_id, user_id, amount):
        """بروزرسانی سکه‌ها"""
        self.get_economy(chat_id, user_id)  # Ensure record exists
        self.cursor.execute('''
            UPDATE economy 
            SET coins = coins + ?
            WHERE chat_id = ? AND user_id = ?
        ''', (amount, chat_id, user_id))
        self.conn.commit()
    
    def update_bank(self, chat_id, user_id, amount):
        """بروزرسانی بانک"""
        self.get_economy(chat_id, user_id)
        self.cursor.execute('''
            UPDATE economy 
            SET bank = bank + ?
            WHERE chat_id = ? AND user_id = ?
        ''', (amount, chat_id, user_id))
        self.conn.commit()
    
    def transfer_coins(self, chat_id, from_user, to_user, amount):
        """انتقال سکه"""
        self.update_coins(chat_id, from_user, -amount)
        self.update_coins(chat_id, to_user, amount)
    
    def set_daily_claimed(self, chat_id, user_id):
        """ثبت دریافت روزانه"""
        self.cursor.execute('''
            UPDATE economy 
            SET daily_claimed = ?
            WHERE chat_id = ? AND user_id = ?
        ''', (datetime.now(), chat_id, user_id))
        self.conn.commit()
    
    def get_richest(self, chat_id, limit=10):
        """دریافت ثروتمندترین‌ها"""
        self.cursor.execute('''
            SELECT user_id, coins + bank as total FROM economy 
            WHERE chat_id = ?
            ORDER BY total DESC
            LIMIT ?
        ''', (chat_id, limit))
        return self.cursor.fetchall()
    
    # ==================== توابع بازی ====================
    
    def create_game(self, chat_id, game_type, game_data, started_by):
        """ایجاد بازی جدید"""
        self.cursor.execute('''
            INSERT INTO games 
            (chat_id, game_type, game_data, started_by)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, game_type, json.dumps(game_data), started_by))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_active_game(self, chat_id, game_type=None):
        """دریافت بازی فعال"""
        if game_type:
            self.cursor.execute('''
                SELECT * FROM games 
                WHERE chat_id = ? AND game_type = ? AND is_active = 1
            ''', (chat_id, game_type))
        else:
            self.cursor.execute('''
                SELECT * FROM games 
                WHERE chat_id = ? AND is_active = 1
            ''', (chat_id,))
        return self.cursor.fetchone()
    
    def update_game(self, game_id, game_data):
        """بروزرسانی بازی"""
        self.cursor.execute('''
            UPDATE games SET game_data = ?
            WHERE id = ?
        ''', (json.dumps(game_data), game_id))
        self.conn.commit()
    
    def end_game(self, game_id, winner_id=None):
        """پایان بازی"""
        self.cursor.execute('''
            UPDATE games 
            SET is_active = 0, ended_at = ?, winner_id = ?
            WHERE id = ?
        ''', (datetime.now(), winner_id, game_id))
        self.conn.commit()
    
    def update_game_score(self, chat_id, user_id, game_type, score=0, win=False):
        """بروزرسانی امتیاز بازی"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO game_scores 
            (chat_id, user_id, game_type)
            VALUES (?, ?, ?)
        ''', (chat_id, user_id, game_type))
        
        if win:
            self.cursor.execute('''
                UPDATE game_scores 
                SET score = score + ?, wins = wins + 1
                WHERE chat_id = ? AND user_id = ? AND game_type = ?
            ''', (score, chat_id, user_id, game_type))
        else:
            self.cursor.execute('''
                UPDATE game_scores 
                SET losses = losses + 1
                WHERE chat_id = ? AND user_id = ? AND game_type = ?
            ''', (chat_id, user_id, game_type))
        self.conn.commit()
    
    def get_game_leaderboard(self, chat_id, game_type, limit=10):
        """دریافت برترین‌های بازی"""
        self.cursor.execute('''
            SELECT user_id, score, wins, losses FROM game_scores 
            WHERE chat_id = ? AND game_type = ?
            ORDER BY wins DESC, score DESC
            LIMIT ?
        ''', (chat_id, game_type, limit))
        return self.cursor.fetchall()
    
    # ==================== توابع AFK ====================
    
    def set_afk(self, user_id, reason=None):
        """تنظیم حالت AFK"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO afk_users 
            (user_id, reason, started_at)
            VALUES (?, ?, ?)
        ''', (user_id, reason, datetime.now()))
        self.conn.commit()
    
    def remove_afk(self, user_id):
        """حذف حالت AFK"""
        self.cursor.execute('DELETE FROM afk_users WHERE user_id = ?', (user_id,))
        self.conn.commit()
    
    def get_afk(self, user_id):
        """دریافت اطلاعات AFK"""
        self.cursor.execute('SELECT * FROM afk_users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    
    # ==================== توابع یادآوری ====================
    
    def add_reminder(self, chat_id, user_id, message, remind_at):
        """اضافه کردن یادآوری"""
        self.cursor.execute('''
            INSERT INTO reminders 
            (chat_id, user_id, message, remind_at)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, user_id, message, remind_at))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_pending_reminders(self):
        """دریافت یادآوری‌های در انتظار"""
        self.cursor.execute('''
            SELECT * FROM reminders 
            WHERE is_sent = 0 AND remind_at <= ?
        ''', (datetime.now(),))
        return self.cursor.fetchall()
    
    def mark_reminder_sent(self, reminder_id):
        """علامت‌گذاری یادآوری به عنوان ارسال شده"""
        self.cursor.execute('''
            UPDATE reminders SET is_sent = 1
            WHERE id = ?
        ''', (reminder_id,))
        self.conn.commit()
    
    def get_user_reminders(self, user_id):
        """دریافت یادآوری‌های کاربر"""
        self.cursor.execute('''
            SELECT * FROM reminders 
            WHERE user_id = ? AND is_sent = 0
        ''', (user_id,))
        return self.cursor.fetchall()
    
    def delete_reminder(self, reminder_id):
        """حذف یادآوری"""
        self.cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
        self.conn.commit()
    
    # ==================== توابع لاگ ====================
    
    def add_log(self, chat_id, user_id, action, details=None):
        """اضافه کردن لاگ"""
        self.cursor.execute('''
            INSERT INTO logs 
            (chat_id, user_id, action, details)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, user_id, action, details))
        self.conn.commit()
    
    def get_logs(self, chat_id, limit=50):
        """دریافت لاگ‌ها"""
        self.cursor.execute('''
            SELECT * FROM logs 
            WHERE chat_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (chat_id, limit))
        return self.cursor.fetchall()
    
    def clear_logs(self, chat_id):
        """پاک کردن لاگ‌ها"""
        self.cursor.execute('DELETE FROM logs WHERE chat_id = ?', (chat_id,))
        self.conn.commit()
    
    # ==================== توابع کلمات ممنوعه ====================
    
    def add_banned_word(self, chat_id, word, action='delete', added_by=None):
        """اضافه کردن کلمه ممنوعه"""
        self.cursor.execute('''
            INSERT INTO banned_words 
            (chat_id, word, action, added_by)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, word.lower(), action, added_by))
        self.conn.commit()
    
    def get_banned_words(self, chat_id):
        """دریافت کلمات ممنوعه"""
        self.cursor.execute('''
            SELECT word, action FROM banned_words WHERE chat_id = ?
        ''', (chat_id,))
        return self.cursor.fetchall()
    
    def remove_banned_word(self, chat_id, word):
        """حذف کلمه ممنوعه"""
        self.cursor.execute('''
            DELETE FROM banned_words 
            WHERE chat_id = ? AND word = ?
        ''', (chat_id, word.lower()))
        self.conn.commit()
    
    # ==================== توابع لینک سفید ====================
    
    def add_whitelist_link(self, chat_id, link, added_by=None):
        """اضافه کردن لینک به لیست سفید"""
        self.cursor.execute('''
            INSERT INTO whitelisted_links 
            (chat_id, link, added_by)
            VALUES (?, ?, ?)
        ''', (chat_id, link, added_by))
        self.conn.commit()
    
    def get_whitelist_links(self, chat_id):
        """دریافت لینک‌های سفید"""
        self.cursor.execute('''
            SELECT link FROM whitelisted_links WHERE chat_id = ?
        ''', (chat_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def remove_whitelist_link(self, chat_id, link):
        """حذف لینک از لیست سفید"""
        self.cursor.execute('''
            DELETE FROM whitelisted_links 
            WHERE chat_id = ? AND link = ?
        ''', (chat_id, link))
        self.conn.commit()
    
    # ==================== توابع قرعه‌کشی ====================
    
    def create_giveaway(self, chat_id, prize, winners_count, ends_at, created_by):
        """ایجاد قرعه‌کشی"""
        self.cursor.execute('''
            INSERT INTO giveaways 
            (chat_id, prize, winners_count, participants, ends_at, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (chat_id, prize, winners_count, json.dumps([]), ends_at, created_by))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def join_giveaway(self, giveaway_id, user_id):
        """شرکت در قرعه‌کشی"""
        self.cursor.execute('SELECT participants FROM giveaways WHERE id = ?', (giveaway_id,))
        result = self.cursor.fetchone()
        if result:
            participants = json.loads(result[0])
            if user_id not in participants:
                participants.append(user_id)
                self.cursor.execute('''
                    UPDATE giveaways SET participants = ?
                    WHERE id = ?
                ''', (json.dumps(participants), giveaway_id))
                self.conn.commit()
                return True
        return False
    
    def get_active_giveaway(self, chat_id):
        """دریافت قرعه‌کشی فعال"""
        self.cursor.execute('''
            SELECT * FROM giveaways 
            WHERE chat_id = ? AND is_active = 1
        ''', (chat_id,))
        return self.cursor.fetchone()
    
    def end_giveaway(self, giveaway_id, winners):
        """پایان قرعه‌کشی"""
        self.cursor.execute('''
            UPDATE giveaways 
            SET is_active = 0, winners = ?
            WHERE id = ?
        ''', (json.dumps(winners), giveaway_id))
        self.conn.commit()
    
    # ==================== توابع سودو ====================
    
    def add_sudo(self, user_id):
        """اضافه کردن سودو"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO sudos (user_id)
            VALUES (?)
        ''', (user_id,))
        self.conn.commit()
    
    def remove_sudo(self, user_id):
        """حذف سودو"""
        self.cursor.execute('DELETE FROM sudos WHERE user_id = ?', (user_id,))
        self.conn.commit()
    
    def get_sudos(self):
        """دریافت لیست سودوها"""
        self.cursor.execute('SELECT user_id FROM sudos')
        return [row[0] for row in self.cursor.fetchall()]
    
    def is_sudo(self, user_id):
        """بررسی سودو بودن"""
        self.cursor.execute('SELECT 1 FROM sudos WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone() is not None
    
    # ==================== توابع گروه مجاز ====================
    
    def add_allowed_group(self, chat_id, added_by):
        """اضافه کردن گروه مجاز"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO allowed_groups (chat_id, added_by)
            VALUES (?, ?)
        ''', (chat_id, added_by))
        self.conn.commit()
    
    def remove_allowed_group(self, chat_id):
        """حذف گروه مجاز"""
        self.cursor.execute('DELETE FROM allowed_groups WHERE chat_id = ?', (chat_id,))
        self.conn.commit()
    
    def is_allowed_group(self, chat_id):
        """بررسی مجاز بودن گروه"""
        self.cursor.execute('SELECT 1 FROM allowed_groups WHERE chat_id = ?', (chat_id,))
        return self.cursor.fetchone() is not None
    
    def get_allowed_groups(self):
        """دریافت لیست گروه‌های مجاز"""
        self.cursor.execute('SELECT chat_id FROM allowed_groups')
        return [row[0] for row in self.cursor.fetchall()]
    
    # ==================== توابع تگ ====================
    
    def create_tag(self, chat_id, tag_name, user_ids, created_by):
        """ایجاد تگ"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO tags 
            (chat_id, tag_name, user_ids, created_by)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, tag_name.lower(), json.dumps(user_ids), created_by))
        self.conn.commit()
    
    def get_tag(self, chat_id, tag_name):
        """دریافت تگ"""
        self.cursor.execute('''
            SELECT user_ids FROM tags 
            WHERE chat_id = ? AND tag_name = ?
        ''', (chat_id, tag_name.lower()))
        result = self.cursor.fetchone()
        return json.loads(result[0]) if result else None
    
    def get_all_tags(self, chat_id):
        """دریافت همه تگ‌ها"""
        self.cursor.execute('SELECT tag_name FROM tags WHERE chat_id = ?', (chat_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def delete_tag(self, chat_id, tag_name):
        """حذف تگ"""
        self.cursor.execute('''
            DELETE FROM tags 
            WHERE chat_id = ? AND tag_name = ?
        ''', (chat_id, tag_name.lower()))
        self.conn.commit()
    
    # ==================== توابع گزارش ====================
    
    def add_report(self, chat_id, reporter_id, reported_user_id, message_id=None, reason=None):
        """اضافه کردن گزارش"""
        self.cursor.execute('''
            INSERT INTO reports 
            (chat_id, reporter_id, reported_user_id, message_id, reason)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, reporter_id, reported_user_id, message_id, reason))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_pending_reports(self, chat_id):
        """دریافت گزارش‌های در انتظار"""
        self.cursor.execute('''
            SELECT * FROM reports 
            WHERE chat_id = ? AND status = 'pending'
        ''', (chat_id,))
        return self.cursor.fetchall()
    
    def resolve_report(self, report_id, resolved_by):
        """حل کردن گزارش"""
        self.cursor.execute('''
            UPDATE reports 
            SET status = 'resolved', resolved_at = ?, resolved_by = ?
            WHERE id = ?
        ''', (datetime.now(), resolved_by, report_id))
        self.conn.commit()
    
    # ==================== توابع بک‌آپ ====================
    
    def create_backup(self, chat_id):
        """ایجاد بک‌آپ"""
        settings = self.get_group_settings(chat_id)
        rules = self.get_group_rules(chat_id)
        welcome = self.get_welcome_message(chat_id)
        goodbye = self.get_goodbye_message(chat_id)
        filters = self.get_all_filters(chat_id)
        notes = self.get_all_notes(chat_id)
        banned_words = self.get_banned_words(chat_id)
        whitelist = self.get_whitelist_links(chat_id)
        
        backup_data = {
            'settings': settings,
            'rules': rules,
            'welcome': welcome,
            'goodbye': goodbye,
            'filters': [{'trigger': f[2], 'response': f[3], 'type': f[4]} for f in filters],
            'notes': [{'name': n[2], 'content': n[3], 'type': n[4]} for n in notes],
            'banned_words': banned_words,
            'whitelist': whitelist
        }
        
        self.cursor.execute('''
            INSERT INTO backups (chat_id, backup_data)
            VALUES (?, ?)
        ''', (chat_id, json.dumps(backup_data)))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def restore_backup(self, chat_id, backup_id):
        """بازیابی بک‌آپ"""
        self.cursor.execute('SELECT backup_data FROM backups WHERE id = ?', (backup_id,))
        result = self.cursor.fetchone()
        if result:
            data = json.loads(result[0])
            
            if data.get('settings'):
                self.update_group_settings(chat_id, data['settings'])
            if data.get('rules'):
                self.set_group_rules(chat_id, data['rules'])
            if data.get('welcome'):
                self.set_welcome_message(chat_id, data['welcome'])
            if data.get('goodbye'):
                self.set_goodbye_message(chat_id, data['goodbye'])
            
            # Restore filters
            self.remove_all_filters(chat_id)
            for f in data.get('filters', []):
                self.add_filter(chat_id, f['trigger'], f['response'], f.get('type', 'text'))
            
            # Restore notes
            self.remove_all_notes(chat_id)
            for n in data.get('notes', []):
                self.add_note(chat_id, n['name'], n['content'], n.get('type', 'text'))
            
            return True
        return False
    
    def get_backups(self, chat_id):
        """دریافت بک‌آپ‌ها"""
        self.cursor.execute('''
            SELECT id, created_at FROM backups 
            WHERE chat_id = ?
            ORDER BY created_at DESC
        ''', (chat_id,))
        return self.cursor.fetchall()
    
    def close(self):
        """بستن اتصال دیتابیس"""
        self.conn.close()


# نمونه گلوبال دیتابیس
db = Database()
