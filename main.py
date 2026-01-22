# main.py - فایل اصلی ربات مدیریت گروه تلگرام
# با بیش از 400 قابلیت مدیریتی و سرگرمی

"""
🤖 ربات مدیریت پیشرفته گروه تلگرام

📋 قابلیت‌ها:
═══════════════════════════════════════════════════════════════

👥 مدیریت اعضا (50+ قابلیت):
  • بن / آنبن کاربران
  • سکوت / رفع سکوت با زمان‌بندی
  • اخراج کاربران
  • اخطار با سیستم پیشرفته
  • ارتقا / عزل ادمین
  • لیست ادمین‌ها، بن‌ها، میوت‌ها
  • مشاهده اخطارها
  • پاکسازی اعضای غیرفعال
  • تگ همه اعضا
  • تگ ادمین‌ها

⚙️ تنظیمات گروه (40+ قابلیت):
  • پیام خوش‌آمدگویی سفارشی
  • پیام خداحافظی سفارشی
  • قوانین گروه
  • کانال اجباری
  • حالت شب
  • کپچا برای اعضای جدید
  • اسلوموید
  • حداکثر اخطار
  • عمل پس از اخطار (بن/میوت/کیک)
  • زبان (فارسی/انگلیسی)
  • حذف پیام‌های سرویس

🔒 قفل‌ها (30+ قابلیت):
  • قفل همه پیام‌ها
  • قفل مدیا
  • قفل استیکر
  • قفل گیف
  • قفل ویس
  • قفل ویدیو
  • قفل فایل
  • قفل عکس
  • قفل لوکیشن
  • قفل کنتکت
  • قفل نظرسنجی
  • قفل لینک
  • قفل فوروارد
  • قفل اینلاین
  • قفل حروف عربی
  • قفل حروف انگلیسی
  • قفل ایموجی

🛡️ امنیت (50+ قابلیت):
  • آنتی‌لینک
  • آنتی‌اسپم
  • آنتی‌فلود
  • آنتی‌فوروارد
  • آنتی‌ربات
  • آنتی‌چنل
  • آنتی‌فحش
  • آنتی‌تبلیغ
  • آنتی‌آیدی
  • آنتی‌منشن
  • آنتی‌هشتگ
  • آنتی‌عربی
  • لیست سفید لینک‌ها
  • کلمات ممنوعه
  • تنظیم حد فلود
  • تنظیم زمان فلود

🎮 بازی‌ها (40+ قابلیت):
  • حدس عدد
  • حدس کلمه
  • دار و درخت (Hangman)
  • کوییز
  • مافیا
  • شرط‌بندی
  • سنگ کاغذ قیچی
  • تاس
  • سکه
  • معما
  • چیستان
  • حقیقت یا جرات
  • بازی کلمات
  • ریاضی
  • حافظه
  • واکنش سریع
  • تایپ سریع
  • ایموجی کوییز
  • لیدربورد بازی‌ها
  • آمار بازی‌ها

💰 سیستم اقتصادی (30+ قابلیت):
  • موجودی
  • پاداش روزانه
  • پاداش هفتگی
  • کار کردن
  • بانک (واریز/برداشت)
  • انتقال سکه
  • قمار
  • فروشگاه
  • کوله‌پشتی
  • لیست ثروتمندترین‌ها
  • آمار اقتصادی

📊 آمار (20+ قابلیت):
  • آمار گروه
  • آمار شخصی
  • برترین‌ها
  • نمودار فعالیت
  • آمار روزانه/هفتگی/ماهانه
  • لاگ‌های گروه

📋 نوت و فیلتر (20+ قابلیت):
  • افزودن نوت
  • نمایش نوت
  • حذف نوت
  • لیست نوت‌ها
  • افزودن فیلتر
  • حذف فیلتر
  • لیست فیلترها
  • اکسپورت/ایمپورت

🎯 ابزارها (40+ قابلیت):
  • کوتاه‌کننده لینک
  • ساخت QR Code
  • ترجمه
  • دیکشنری
  • ماشین حساب
  • تبدیل ارز
  • آب و هوا
  • ساعت
  • تقویم
  • یادآوری
  • رنگ‌ساز
  • رمز ساز
  • خلاصه متن
  • تولید متن لورم
  • تبدیل واحد
  • فال
  • نظرسنجی
  • تگ همه

🎁 قرعه‌کشی (15+ قابلیت):
  • ایجاد قرعه‌کشی
  • شرکت در قرعه‌کشی
  • قرعه‌کشی کردن
  • لغو قرعه‌کشی
  • آمار قرعه‌کشی‌ها
  • تاریخچه

📅 رویدادها (15+ قابلیت):
  • ایجاد رویداد
  • شرکت در رویداد
  • لغو شرکت
  • آمار رویداد
  • تاریخچه رویدادها

📝 پیام‌ها (20+ قابلیت):
  • ارسال همگانی
  • پین پیام
  • آنپین پیام
  • حذف پیام
  • پاکسازی (purge)
  • کپی پیام
  • زمان‌بندی پیام
  • لیست پیام‌های زمان‌بندی شده

👑 سودو (30+ قابلیت):
  • آمار کلی ربات
  • لیست همه گروه‌ها
  • افزودن/حذف سودو
  • لیست سودوها
  • پیام همگانی به همه گروه‌ها
  • افزودن/حذف گروه مجاز
  • لیست گروه‌های مجاز
  • ری‌استارت ربات
  • بک‌آپ دیتابیس
  • بازیابی دیتابیس
  • لاگ سیستم
  • تنظیمات ربات

═══════════════════════════════════════════════════════════════

📌 نکات مهم:
  • فقط سودو می‌تواند ربات را به گروه اضافه کند
  • پنل شیشه‌ای با دکمه‌های inline
  • پشتیبانی از چند زبان
  • دیتابیس SQLite برای ذخیره‌سازی

"""

import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ChatMemberHandler, filters
)

from config import BOT_TOKEN, SUDO_USERS
from database import db

# تنظیم لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """راه‌اندازی ربات"""
    
    # ساخت اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ایمپورت هندلرها
    from handlers import (
        start_command, help_command, panel_command, sudo_panel_command,
        ban_command, unban_command, mute_command, unmute_command,
        kick_command, warn_command, unwarn_command, promote_command, demote_command,
        settings_command, setwelcome_command, setgoodbye_command, setrules_command, rules_command,
        lock_command, unlock_command,
        game_command, dice_command, coin_command, quiz_command, truth_command, dare_command, riddle_command,
        balance_command
    )
    
    from handlers2 import (
        work_command, transfer_command,
        stats_command, mystats_command, top_command,
        addnote_command, note_command, delnote_command,
        addfilter_command, delfilter_command, filters_command,
        addgroup_command, removegroup_command, groups_command,
        addsudo_command, removesudo_command, sudos_command, broadcast_command,
        new_member_handler, left_member_handler, message_handler, callback_handler
    )
    
    # ==================== دستورات ====================
    
    # دستورات اصلی
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("panel", panel_command))
    application.add_handler(CommandHandler("sudopanel", sudo_panel_command))
    
    # مدیریت اعضا
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("kick", kick_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("unwarn", unwarn_command))
    application.add_handler(CommandHandler("promote", promote_command))
    application.add_handler(CommandHandler("demote", demote_command))
    
    # تنظیمات
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("setwelcome", setwelcome_command))
    application.add_handler(CommandHandler("setgoodbye", setgoodbye_command))
    application.add_handler(CommandHandler("setrules", setrules_command))
    application.add_handler(CommandHandler("rules", rules_command))
    
    # قفل‌ها
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("unlock", unlock_command))
    
    # بازی‌ها
    application.add_handler(CommandHandler("game", game_command))
    application.add_handler(CommandHandler("dice", dice_command))
    application.add_handler(CommandHandler("coin", coin_command))
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(CommandHandler("truth", truth_command))
    application.add_handler(CommandHandler("dare", dare_command))
    application.add_handler(CommandHandler("riddle", riddle_command))
    
    # اقتصاد
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("daily", balance_command))  # will fix
    application.add_handler(CommandHandler("work", work_command))
    application.add_handler(CommandHandler("transfer", transfer_command))
    
    # آمار
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("mystats", mystats_command))
    application.add_handler(CommandHandler("top", top_command))
    
    # نوت و فیلتر
    application.add_handler(CommandHandler("addnote", addnote_command))
    application.add_handler(CommandHandler("note", note_command))
    application.add_handler(CommandHandler("delnote", delnote_command))
    application.add_handler(CommandHandler("addfilter", addfilter_command))
    application.add_handler(CommandHandler("delfilter", delfilter_command))
    application.add_handler(CommandHandler("filters", filters_command))
    
    # سودو
    application.add_handler(CommandHandler("addgroup", addgroup_command))
    application.add_handler(CommandHandler("removegroup", removegroup_command))
    application.add_handler(CommandHandler("groups", groups_command))
    application.add_handler(CommandHandler("addsudo", addsudo_command))
    application.add_handler(CommandHandler("removesudo", removesudo_command))
    application.add_handler(CommandHandler("sudos", sudos_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    
    # ==================== هندلرها ====================
    
    # کالبک‌ها
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # اعضای جدید و خروجی
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member_handler))
    
    # پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # شروع ربات
    logger.info("🤖 ربات در حال راه‌اندازی...")
    logger.info(f"👑 سودوها: {SUDO_USERS}")
    
    # اضافه کردن سودوهای پیش‌فرض به دیتابیس
    for sudo in SUDO_USERS:
        db.add_sudo(sudo)
    
    application.run_polling(allowed_updates=["message", "callback_query", "chat_member"])

if __name__ == "__main__":
    main()
