# keyboards.py - کیبوردهای شیشه‌ای و inline

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    """کلاس مدیریت کیبوردها با طراحی شیشه‌ای"""
    
    # ==================== پنل اصلی ====================
    
    @staticmethod
    def main_panel():
        """پنل اصلی مدیریت - شیشه‌ای"""
        keyboard = [
            [InlineKeyboardButton("╔═══════════════════════════╗", callback_data="h")],
            [InlineKeyboardButton("║  🎛 پنل مدیریت گروه  ║", callback_data="h2")],
            [InlineKeyboardButton("╚═══════════════════════════╝", callback_data="h3")],
            [
                InlineKeyboardButton("👥 مدیریت اعضا", callback_data="panel_members"),
                InlineKeyboardButton("⚙️ تنظیمات", callback_data="panel_settings")
            ],
            [
                InlineKeyboardButton("🔒 قفل‌ها", callback_data="panel_locks"),
                InlineKeyboardButton("🛡️ امنیت", callback_data="panel_security")
            ],
            [
                InlineKeyboardButton("📝 پیام‌ها", callback_data="panel_messages"),
                InlineKeyboardButton("🎮 بازی‌ها", callback_data="panel_games")
            ],
            [
                InlineKeyboardButton("💰 اقتصاد", callback_data="panel_economy"),
                InlineKeyboardButton("📊 آمار", callback_data="panel_stats")
            ],
            [
                InlineKeyboardButton("🎯 ابزارها", callback_data="panel_tools"),
                InlineKeyboardButton("📋 نوت و فیلتر", callback_data="panel_notes")
            ],
            [
                InlineKeyboardButton("🎁 قرعه‌کشی", callback_data="panel_giveaway"),
                InlineKeyboardButton("📅 رویدادها", callback_data="panel_events")
            ],
            [InlineKeyboardButton("═══════════════════════════", callback_data="f")],
            [InlineKeyboardButton("❌ بستن پنل", callback_data="close_panel")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل مدیریت اعضا ====================
    
    @staticmethod
    def members_panel():
        """پنل مدیریت اعضا"""
        keyboard = [
            [InlineKeyboardButton("╔══════ 👥 مدیریت اعضا ══════╗", callback_data="h")],
            [
                InlineKeyboardButton("🔇 سکوت", callback_data="action_mute"),
                InlineKeyboardButton("🔊 رفع سکوت", callback_data="action_unmute")
            ],
            [
                InlineKeyboardButton("🚫 بن", callback_data="action_ban"),
                InlineKeyboardButton("✅ آنبن", callback_data="action_unban")
            ],
            [
                InlineKeyboardButton("👢 کیک", callback_data="action_kick"),
                InlineKeyboardButton("⚡ اخطار", callback_data="action_warn")
            ],
            [
                InlineKeyboardButton("🗑️ حذف اخطار", callback_data="action_delwarn"),
                InlineKeyboardButton("🔄 ریست اخطار", callback_data="action_resetwarn")
            ],
            [
                InlineKeyboardButton("👑 ادمین کردن", callback_data="action_promote"),
                InlineKeyboardButton("📉 عزل ادمین", callback_data="action_demote")
            ],
            [
                InlineKeyboardButton("📋 لیست ادمین‌ها", callback_data="list_admins"),
                InlineKeyboardButton("🚫 لیست بن‌ها", callback_data="list_bans")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل تنظیمات ====================
    
    @staticmethod
    def settings_panel(settings):
        """پنل تنظیمات گروه"""
        def status(key):
            return "✅" if settings.get(key, False) else "❌"
        
        keyboard = [
            [InlineKeyboardButton("╔════════ ⚙️ تنظیمات ════════╗", callback_data="h")],
            [
                InlineKeyboardButton(f"خوش‌آمد {status('welcome_enabled')}", callback_data="toggle_welcome"),
                InlineKeyboardButton(f"خداحافظی {status('goodbye_enabled')}", callback_data="toggle_goodbye")
            ],
            [
                InlineKeyboardButton(f"حذف سرویس {status('auto_delete_service')}", callback_data="toggle_service"),
                InlineKeyboardButton(f"حالت شب {status('night_mode_enabled')}", callback_data="toggle_night")
            ],
            [
                InlineKeyboardButton(f"کپچا {status('captcha_enabled')}", callback_data="toggle_captcha"),
                InlineKeyboardButton(f"اسلوموید {settings.get('slow_mode', 0)}ث", callback_data="set_slowmode")
            ],
            [
                InlineKeyboardButton("📝 تنظیم خوش‌آمد", callback_data="set_welcome"),
                InlineKeyboardButton("📝 تنظیم خداحافظی", callback_data="set_goodbye")
            ],
            [
                InlineKeyboardButton("📜 تنظیم قوانین", callback_data="set_rules"),
                InlineKeyboardButton("📢 کانال اجباری", callback_data="set_forcejoin")
            ],
            [
                InlineKeyboardButton(f"⚡ حداکثر اخطار: {settings.get('max_warn', 3)}", callback_data="set_maxwarn"),
                InlineKeyboardButton(f"عمل اخطار: {settings.get('warn_action', 'mute')}", callback_data="set_warnaction")
            ],
            [
                InlineKeyboardButton("🌐 زبان", callback_data="set_language")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل قفل‌ها ====================
    
    @staticmethod
    def locks_panel(settings):
        """پنل قفل‌های گروه"""
        def status(key):
            return "🔒" if settings.get(key, False) else "🔓"
        
        keyboard = [
            [InlineKeyboardButton("╔════════ 🔒 قفل‌ها ════════╗", callback_data="h")],
            [
                InlineKeyboardButton(f"همه {status('lock_all')}", callback_data="toggle_lock_all"),
                InlineKeyboardButton(f"مدیا {status('lock_media')}", callback_data="toggle_lock_media")
            ],
            [
                InlineKeyboardButton(f"استیکر {status('lock_sticker')}", callback_data="toggle_lock_sticker"),
                InlineKeyboardButton(f"گیف {status('lock_gif')}", callback_data="toggle_lock_gif")
            ],
            [
                InlineKeyboardButton(f"ویس {status('lock_voice')}", callback_data="toggle_lock_voice"),
                InlineKeyboardButton(f"ویدیو {status('lock_video')}", callback_data="toggle_lock_video")
            ],
            [
                InlineKeyboardButton(f"فایل {status('lock_document')}", callback_data="toggle_lock_document"),
                InlineKeyboardButton(f"عکس {status('lock_photo')}", callback_data="toggle_lock_photo")
            ],
            [
                InlineKeyboardButton(f"لوکیشن {status('lock_location')}", callback_data="toggle_lock_location"),
                InlineKeyboardButton(f"کنتکت {status('lock_contact')}", callback_data="toggle_lock_contact")
            ],
            [
                InlineKeyboardButton(f"نظرسنجی {status('lock_poll')}", callback_data="toggle_lock_poll"),
                InlineKeyboardButton(f"لینک {status('lock_url')}", callback_data="toggle_lock_url")
            ],
            [
                InlineKeyboardButton(f"فوروارد {status('lock_forward')}", callback_data="toggle_lock_forward"),
                InlineKeyboardButton(f"اینلاین {status('lock_inline')}", callback_data="toggle_lock_inline")
            ],
            [
                InlineKeyboardButton("🔒 قفل همه", callback_data="lock_all_types"),
                InlineKeyboardButton("🔓 باز همه", callback_data="unlock_all_types")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل امنیت ====================
    
    @staticmethod
    def security_panel(settings):
        """پنل امنیتی"""
        def status(key):
            return "✅" if settings.get(key, False) else "❌"
        
        keyboard = [
            [InlineKeyboardButton("╔════════ 🛡️ امنیت ════════╗", callback_data="h")],
            [
                InlineKeyboardButton(f"آنتی‌لینک {status('antilink_enabled')}", callback_data="toggle_antilink"),
                InlineKeyboardButton(f"آنتی‌اسپم {status('antispam_enabled')}", callback_data="toggle_antispam")
            ],
            [
                InlineKeyboardButton(f"آنتی‌فلود {status('antiflood_enabled')}", callback_data="toggle_antiflood"),
                InlineKeyboardButton(f"آنتی‌فوروارد {status('antiforward_enabled')}", callback_data="toggle_antiforward")
            ],
            [
                InlineKeyboardButton(f"آنتی‌ربات {status('antibot_enabled')}", callback_data="toggle_antibot"),
                InlineKeyboardButton(f"آنتی‌فحش {status('antiswear_enabled')}", callback_data="toggle_antiswear")
            ],
            [
                InlineKeyboardButton(f"آنتی‌تبلیغ {status('antiad_enabled')}", callback_data="toggle_antiad"),
                InlineKeyboardButton(f"آنتی‌آیدی {status('antiid_enabled')}", callback_data="toggle_antiid")
            ],
            [
                InlineKeyboardButton("➕ لینک سفید", callback_data="whitelist_add"),
                InlineKeyboardButton("📋 لیست سفید", callback_data="whitelist_list")
            ],
            [
                InlineKeyboardButton("➕ کلمه ممنوعه", callback_data="badword_add"),
                InlineKeyboardButton("📋 کلمات ممنوعه", callback_data="badword_list")
            ],
            [
                InlineKeyboardButton(f"⚡ حد فلود: {settings.get('flood_limit', 5)}", callback_data="set_floodlimit"),
                InlineKeyboardButton(f"⏱ زمان فلود: {settings.get('flood_time', 10)}ث", callback_data="set_floodtime")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل بازی‌ها ====================
    
    @staticmethod
    def games_panel():
        """پنل بازی‌ها"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 🎮 بازی‌ها ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("🔢 حدس عدد", callback_data="game_guess_number"),
                InlineKeyboardButton("📝 حدس کلمه", callback_data="game_guess_word")
            ],
            [
                InlineKeyboardButton("🎯 دار و درخت", callback_data="game_hangman"),
                InlineKeyboardButton("❓ کوییز", callback_data="game_quiz")
            ],
            [
                InlineKeyboardButton("🎭 مافیا", callback_data="game_mafia"),
                InlineKeyboardButton("💰 شرط‌بندی", callback_data="game_bet")
            ],
            [
                InlineKeyboardButton("✂️ سنگ کاغذ قیچی", callback_data="game_rps"),
                InlineKeyboardButton("🎲 تاس", callback_data="game_dice")
            ],
            [
                InlineKeyboardButton("🪙 سکه", callback_data="game_coin"),
                InlineKeyboardButton("🧩 معما", callback_data="game_riddle")
            ],
            [
                InlineKeyboardButton("💡 چیستان", callback_data="game_puzzle"),
                InlineKeyboardButton("🎭 حقیقت یا جرات", callback_data="game_truth_dare")
            ],
            [
                InlineKeyboardButton("🔤 بازی کلمات", callback_data="game_word_chain"),
                InlineKeyboardButton("➕ ریاضی", callback_data="game_math")
            ],
            [
                InlineKeyboardButton("🧠 حافظه", callback_data="game_memory"),
                InlineKeyboardButton("⚡ واکنش سریع", callback_data="game_reaction")
            ],
            [
                InlineKeyboardButton("🏆 برترین‌ها", callback_data="game_leaderboard")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل اقتصاد ====================
    
    @staticmethod
    def economy_panel():
        """پنل اقتصادی"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 💰 اقتصاد ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("💵 موجودی", callback_data="eco_balance"),
                InlineKeyboardButton("🎁 روزانه", callback_data="eco_daily")
            ],
            [
                InlineKeyboardButton("📅 هفتگی", callback_data="eco_weekly"),
                InlineKeyboardButton("💼 کار", callback_data="eco_work")
            ],
            [
                InlineKeyboardButton("🏦 بانک", callback_data="eco_bank"),
                InlineKeyboardButton("💸 برداشت", callback_data="eco_withdraw")
            ],
            [
                InlineKeyboardButton("💱 انتقال", callback_data="eco_transfer"),
                InlineKeyboardButton("🎰 قمار", callback_data="eco_gamble")
            ],
            [
                InlineKeyboardButton("🛒 فروشگاه", callback_data="eco_shop"),
                InlineKeyboardButton("🎒 کوله‌پشتی", callback_data="eco_inventory")
            ],
            [
                InlineKeyboardButton("🏆 ثروتمندترین‌ها", callback_data="eco_richest")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل آمار ====================
    
    @staticmethod
    def stats_panel():
        """پنل آمار"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 📊 آمار ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("👥 آمار گروه", callback_data="stats_group"),
                InlineKeyboardButton("👤 آمار من", callback_data="stats_me")
            ],
            [
                InlineKeyboardButton("🏆 برترین‌ها", callback_data="stats_top"),
                InlineKeyboardButton("📈 نمودار فعالیت", callback_data="stats_chart")
            ],
            [
                InlineKeyboardButton("📅 آمار روزانه", callback_data="stats_daily"),
                InlineKeyboardButton("📆 آمار هفتگی", callback_data="stats_weekly")
            ],
            [
                InlineKeyboardButton("📋 لاگ‌ها", callback_data="stats_logs")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل ابزارها ====================
    
    @staticmethod
    def tools_panel():
        """پنل ابزارها"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 🎯 ابزارها ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("🔗 کوتاه‌کننده لینک", callback_data="tool_shorturl"),
                InlineKeyboardButton("🔍 QR ساز", callback_data="tool_qr")
            ],
            [
                InlineKeyboardButton("🌐 ترجمه", callback_data="tool_translate"),
                InlineKeyboardButton("📖 دیکشنری", callback_data="tool_dictionary")
            ],
            [
                InlineKeyboardButton("🔢 ماشین حساب", callback_data="tool_calc"),
                InlineKeyboardButton("💱 تبدیل ارز", callback_data="tool_currency")
            ],
            [
                InlineKeyboardButton("🌤 آب و هوا", callback_data="tool_weather"),
                InlineKeyboardButton("⏰ زمان", callback_data="tool_time")
            ],
            [
                InlineKeyboardButton("📅 تقویم", callback_data="tool_calendar"),
                InlineKeyboardButton("⏱ یادآوری", callback_data="tool_reminder")
            ],
            [
                InlineKeyboardButton("🔐 رمز ساز", callback_data="tool_password"),
                InlineKeyboardButton("🎭 فال", callback_data="tool_fortune")
            ],
            [
                InlineKeyboardButton("📊 نظرسنجی", callback_data="tool_poll"),
                InlineKeyboardButton("🏷️ تگ همه", callback_data="tool_tagall")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل نوت و فیلتر ====================
    
    @staticmethod
    def notes_panel():
        """پنل نوت و فیلتر"""
        keyboard = [
            [InlineKeyboardButton("╔════ 📋 نوت و فیلتر ════╗", callback_data="h")],
            [
                InlineKeyboardButton("📝 افزودن نوت", callback_data="note_add"),
                InlineKeyboardButton("📋 لیست نوت‌ها", callback_data="note_list")
            ],
            [
                InlineKeyboardButton("🗑️ حذف نوت", callback_data="note_delete"),
                InlineKeyboardButton("🗑️ حذف همه نوت", callback_data="note_deleteall")
            ],
            [
                InlineKeyboardButton("🔍 افزودن فیلتر", callback_data="filter_add"),
                InlineKeyboardButton("📋 لیست فیلترها", callback_data="filter_list")
            ],
            [
                InlineKeyboardButton("🗑️ حذف فیلتر", callback_data="filter_delete"),
                InlineKeyboardButton("🗑️ حذف همه فیلتر", callback_data="filter_deleteall")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل قرعه‌کشی ====================
    
    @staticmethod
    def giveaway_panel():
        """پنل قرعه‌کشی"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 🎁 قرعه‌کشی ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("🆕 ایجاد قرعه‌کشی", callback_data="giveaway_create"),
                InlineKeyboardButton("📋 قرعه‌کشی فعال", callback_data="giveaway_active")
            ],
            [
                InlineKeyboardButton("🎯 قرعه‌کشی کردن", callback_data="giveaway_draw"),
                InlineKeyboardButton("❌ لغو قرعه‌کشی", callback_data="giveaway_cancel")
            ],
            [
                InlineKeyboardButton("📊 آمار قرعه‌کشی‌ها", callback_data="giveaway_stats"),
                InlineKeyboardButton("📜 تاریخچه", callback_data="giveaway_history")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل رویدادها ====================
    
    @staticmethod
    def events_panel():
        """پنل رویدادها"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 📅 رویدادها ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("🆕 ایجاد رویداد", callback_data="event_create"),
                InlineKeyboardButton("📋 رویدادهای فعال", callback_data="event_active")
            ],
            [
                InlineKeyboardButton("✅ شرکت در رویداد", callback_data="event_join"),
                InlineKeyboardButton("❌ لغو شرکت", callback_data="event_leave")
            ],
            [
                InlineKeyboardButton("📊 آمار رویداد", callback_data="event_stats"),
                InlineKeyboardButton("📜 تاریخچه", callback_data="event_history")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل پیام‌ها ====================
    
    @staticmethod
    def messages_panel():
        """پنل پیام‌ها"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 📝 پیام‌ها ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("📢 ارسال همگانی", callback_data="msg_broadcast"),
                InlineKeyboardButton("📌 پین پیام", callback_data="msg_pin")
            ],
            [
                InlineKeyboardButton("📍 آنپین پیام", callback_data="msg_unpin"),
                InlineKeyboardButton("🗑️ حذف پیام", callback_data="msg_delete")
            ],
            [
                InlineKeyboardButton("🗑️ پاکسازی", callback_data="msg_purge"),
                InlineKeyboardButton("📋 کپی پیام", callback_data="msg_copy")
            ],
            [
                InlineKeyboardButton("⏰ زمان‌بندی پیام", callback_data="msg_schedule"),
                InlineKeyboardButton("📋 پیام‌های زمان‌بندی", callback_data="msg_scheduled_list")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== پنل سودو ====================
    
    @staticmethod
    def sudo_panel():
        """پنل سودو"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 👑 پنل سودو ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("📊 آمار کل", callback_data="sudo_stats"),
                InlineKeyboardButton("👥 لیست گروه‌ها", callback_data="sudo_groups")
            ],
            [
                InlineKeyboardButton("➕ افزودن سودو", callback_data="sudo_add"),
                InlineKeyboardButton("➖ حذف سودو", callback_data="sudo_remove")
            ],
            [
                InlineKeyboardButton("📋 لیست سودوها", callback_data="sudo_list"),
                InlineKeyboardButton("📢 پیام همگانی", callback_data="sudo_broadcast")
            ],
            [
                InlineKeyboardButton("➕ افزودن گروه مجاز", callback_data="sudo_addgroup"),
                InlineKeyboardButton("➖ حذف گروه مجاز", callback_data="sudo_removegroup")
            ],
            [
                InlineKeyboardButton("📋 گروه‌های مجاز", callback_data="sudo_allowedgroups"),
                InlineKeyboardButton("🔄 ری‌استارت", callback_data="sudo_restart")
            ],
            [
                InlineKeyboardButton("💾 بک‌آپ", callback_data="sudo_backup"),
                InlineKeyboardButton("📥 بازیابی", callback_data="sudo_restore")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("❌ بستن", callback_data="close_panel")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد کپچا ====================
    
    @staticmethod
    def captcha_keyboard(options):
        """کیبورد کپچا"""
        keyboard = []
        row = []
        for option in options:
            row.append(InlineKeyboardButton(str(option), callback_data=f"captcha_{option}"))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد تأیید ====================
    
    @staticmethod
    def confirm_keyboard(action, data=""):
        """کیبورد تأیید"""
        keyboard = [
            [
                InlineKeyboardButton("✅ تأیید", callback_data=f"confirm_{action}_{data}"),
                InlineKeyboardButton("❌ لغو", callback_data="cancel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد بستن ====================
    
    @staticmethod
    def close_keyboard():
        """کیبورد بستن"""
        keyboard = [[InlineKeyboardButton("❌ بستن", callback_data="close_panel")]]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد شرکت در قرعه‌کشی ====================
    
    @staticmethod
    def join_giveaway_keyboard(giveaway_id, participants_count):
        """کیبورد شرکت در قرعه‌کشی"""
        keyboard = [[
            InlineKeyboardButton(f"🎁 شرکت در قرعه‌کشی ({participants_count} نفر)", 
                               callback_data=f"join_giveaway_{giveaway_id}")
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد سنگ کاغذ قیچی ====================
    
    @staticmethod
    def rps_keyboard(game_id):
        """کیبورد سنگ کاغذ قیچی"""
        keyboard = [[
            InlineKeyboardButton("🪨 سنگ", callback_data=f"rps_rock_{game_id}"),
            InlineKeyboardButton("📄 کاغذ", callback_data=f"rps_paper_{game_id}"),
            InlineKeyboardButton("✂️ قیچی", callback_data=f"rps_scissors_{game_id}")
        ]]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد حقیقت یا جرات ====================
    
    @staticmethod
    def truth_dare_keyboard():
        """کیبورد حقیقت یا جرات"""
        keyboard = [
            [
                InlineKeyboardButton("💭 حقیقت", callback_data="td_truth"),
                InlineKeyboardButton("🎯 جرات", callback_data="td_dare")
            ],
            [InlineKeyboardButton("🔄 تصادفی", callback_data="td_random")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد راهنما ====================
    
    @staticmethod
    def help_keyboard():
        """کیبورد راهنما"""
        keyboard = [
            [InlineKeyboardButton("╔════════ 📚 راهنما ════════╗", callback_data="h")],
            [
                InlineKeyboardButton("👥 مدیریت اعضا", callback_data="help_members"),
                InlineKeyboardButton("⚙️ تنظیمات", callback_data="help_settings")
            ],
            [
                InlineKeyboardButton("🔒 قفل‌ها", callback_data="help_locks"),
                InlineKeyboardButton("🛡️ امنیت", callback_data="help_security")
            ],
            [
                InlineKeyboardButton("🎮 بازی‌ها", callback_data="help_games"),
                InlineKeyboardButton("💰 اقتصاد", callback_data="help_economy")
            ],
            [
                InlineKeyboardButton("📋 نوت و فیلتر", callback_data="help_notes"),
                InlineKeyboardButton("🎯 ابزارها", callback_data="help_tools")
            ],
            [InlineKeyboardButton("╚════════════════════════════╝", callback_data="f")],
            [InlineKeyboardButton("❌ بستن", callback_data="close_panel")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد انتخاب زبان ====================
    
    @staticmethod
    def language_keyboard():
        """کیبورد انتخاب زبان"""
        keyboard = [
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_settings")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد زمان سکوت ====================
    
    @staticmethod
    def mute_time_keyboard():
        """کیبورد انتخاب زمان سکوت"""
        keyboard = [
            [
                InlineKeyboardButton("5 دقیقه", callback_data="mutetime_5m"),
                InlineKeyboardButton("15 دقیقه", callback_data="mutetime_15m"),
                InlineKeyboardButton("30 دقیقه", callback_data="mutetime_30m")
            ],
            [
                InlineKeyboardButton("1 ساعت", callback_data="mutetime_1h"),
                InlineKeyboardButton("6 ساعت", callback_data="mutetime_6h"),
                InlineKeyboardButton("12 ساعت", callback_data="mutetime_12h")
            ],
            [
                InlineKeyboardButton("1 روز", callback_data="mutetime_1d"),
                InlineKeyboardButton("1 هفته", callback_data="mutetime_1w"),
                InlineKeyboardButton("♾ همیشه", callback_data="mutetime_forever")
            ],
            [InlineKeyboardButton("❌ لغو", callback_data="cancel")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد اسلوموید ====================
    
    @staticmethod
    def slowmode_keyboard():
        """کیبورد انتخاب اسلوموید"""
        keyboard = [
            [
                InlineKeyboardButton("خاموش", callback_data="slowmode_0"),
                InlineKeyboardButton("10 ثانیه", callback_data="slowmode_10"),
                InlineKeyboardButton("30 ثانیه", callback_data="slowmode_30")
            ],
            [
                InlineKeyboardButton("1 دقیقه", callback_data="slowmode_60"),
                InlineKeyboardButton("5 دقیقه", callback_data="slowmode_300"),
                InlineKeyboardButton("15 دقیقه", callback_data="slowmode_900")
            ],
            [InlineKeyboardButton("1 ساعت", callback_data="slowmode_3600")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_settings")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # ==================== کیبورد عضویت در کانال ====================
    
    @staticmethod
    def force_join_keyboard(channel_username):
        """کیبورد عضویت اجباری"""
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{channel_username}")],
            [InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")]
        ]
        return InlineKeyboardMarkup(keyboard)
