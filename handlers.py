# handlers.py - هندلرهای اصلی ربات

import random
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatMemberStatus

from config import SUDO_USERS, TEXTS
from database import db
from keyboards import Keyboards
from utils import (
    parse_time, format_time, get_user_mention, escape_html,
    format_welcome, format_stats_message, format_user_stats,
    format_leaderboard, calculate_daily_reward, calculate_work_reward,
    get_truth, get_dare, get_riddle, get_quiz, roll_dice, flip_coin,
    generate_captcha_math, check_bad_words, is_whitelisted_link,
    extract_links, contains_link
)

# ==================== دکوراتورها ====================

def sudo_only(func):
    """فقط سودو"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in SUDO_USERS and not db.is_sudo(user_id):
            await update.message.reply_text("❌ این دستور فقط برای سودو ربات است.")
            return
        return await func(update, context)
    return wrapper

def admin_only(func):
    """فقط ادمین"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        user = update.effective_user
        if user.id in SUDO_USERS or db.is_sudo(user.id):
            return await func(update, context)
        member = await chat.get_member(user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await update.message.reply_text("❌ این دستور فقط برای ادمین‌ها است.")
            return
        return await func(update, context)
    return wrapper

def group_only(func):
    """فقط گروه"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("❌ این دستور فقط در گروه کار می‌کند.")
            return
        return await func(update, context)
    return wrapper

# ==================== دستورات اصلی ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور شروع"""
    user = update.effective_user
    chat = update.effective_chat
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    if chat.type == 'private':
        text = f"""
╔══════════════════════════════╗
║  🤖 ربات مدیریت پیشرفته گروه ║
╠══════════════════════════════╣
║ سلام {escape_html(user.first_name)}! 👋
║
║ من یک ربات مدیریت گروه با
║ بیش از 400 قابلیت هستم!
║
║ 📌 قابلیت‌های اصلی:
║ • مدیریت اعضا (بن، میوت، ...)
║ • امنیت (آنتی‌اسپم، آنتی‌لینک)
║ • بازی‌های متنوع
║ • سیستم اقتصادی
║ • قرعه‌کشی و رویدادها
║ • و صدها قابلیت دیگر...
╚══════════════════════════════╝

⚠️ توجه: فقط سودو ربات می‌تواند 
ربات را به گروه اضافه کند.
"""
        keyboard = Keyboards.help_keyboard()
    else:
        text = "✅ برای مشاهده پنل از /panel استفاده کنید."
        keyboard = Keyboards.close_keyboard()
    
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور راهنما"""
    text = """
📚 راهنمای دستورات

👥 مدیریت اعضا:
/ban /unban /mute /unmute /kick
/warn /unwarn /promote /demote

⚙️ تنظیمات:
/settings /setwelcome /setgoodbye
/setrules /rules

🔒 قفل‌ها:
/lock /unlock

🎮 بازی‌ها:
/game /quiz /dice /coin /truth /dare

💰 اقتصاد:
/balance /daily /work /transfer

📊 آمار:
/stats /mystats /top

🎛 پنل:
/panel - پنل مدیریت
"""
    await update.message.reply_text(text, reply_markup=Keyboards.help_keyboard())

@group_only
@admin_only
async def panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش پنل مدیریت"""
    await update.message.reply_text("🎛 پنل مدیریت گروه", reply_markup=Keyboards.main_panel())

@sudo_only
async def sudo_panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش پنل سودو"""
    await update.message.reply_text("👑 پنل سودو", reply_markup=Keyboards.sudo_panel())

# ==================== مدیریت اعضا ====================

@group_only
@admin_only
async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بن کردن کاربر"""
    chat = update.effective_chat
    user = update.effective_user
    message = update.message
    target_user = None
    reason = "بدون دلیل"
    
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        if context.args:
            reason = ' '.join(context.args)
    elif context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
            if len(context.args) > 1:
                reason = ' '.join(context.args[1:])
        except:
            await message.reply_text("❌ کاربر یافت نشد.")
            return
    else:
        await message.reply_text("❌ روی پیام ریپلای کنید یا آیدی وارد کنید.")
        return
    
    if target_user.id in SUDO_USERS or db.is_sudo(target_user.id):
        await message.reply_text("❌ نمی‌توانید سودو را بن کنید!")
        return
    
    try:
        await chat.ban_member(target_user.id)
        db.ban_user(chat.id, target_user.id, reason)
        db.add_log(chat.id, user.id, "ban", f"Banned {target_user.id}")
        await message.reply_text(
            f"🚫 {get_user_mention(target_user)} بن شد.\n📝 دلیل: {reason}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

@group_only
@admin_only
async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """آنبن کردن کاربر"""
    chat = update.effective_chat
    message = update.message
    
    if not context.args:
        await message.reply_text("❌ آیدی را وارد کنید.")
        return
    
    try:
        target_id = int(context.args[0])
        await chat.unban_member(target_id)
        db.unban_user(chat.id, target_id)
        await message.reply_text(f"✅ کاربر {target_id} آنبن شد.")
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

@group_only
@admin_only
async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """سکوت کردن کاربر"""
    chat = update.effective_chat
    user = update.effective_user
    message = update.message
    target_user = None
    duration = None
    
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        if context.args:
            duration = parse_time(context.args[0])
    elif context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
            if len(context.args) > 1:
                duration = parse_time(context.args[1])
        except:
            await message.reply_text("❌ کاربر یافت نشد.")
            return
    else:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    if target_user.id in SUDO_USERS or db.is_sudo(target_user.id):
        await message.reply_text("❌ نمی‌توانید سودو را سکوت کنید!")
        return
    
    try:
        until = datetime.now() + timedelta(seconds=duration) if duration else None
        await chat.restrict_member(
            target_user.id,
            ChatPermissions(can_send_messages=False),
            until_date=until
        )
        db.mute_user(chat.id, target_user.id, until)
        time_str = format_time(duration) if duration else "همیشگی"
        await message.reply_text(
            f"🔇 {get_user_mention(target_user)} سکوت شد.\n⏱ مدت: {time_str}",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

@group_only
@admin_only
async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رفع سکوت کاربر"""
    chat = update.effective_chat
    message = update.message
    target_user = None
    
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    elif context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
        except:
            await message.reply_text("❌ کاربر یافت نشد.")
            return
    else:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    try:
        await chat.restrict_member(
            target_user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        db.unmute_user(chat.id, target_user.id)
        await message.reply_text(
            f"🔊 {get_user_mention(target_user)} از سکوت خارج شد.",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

@group_only
@admin_only
async def kick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اخراج کاربر"""
    chat = update.effective_chat
    message = update.message
    target_user = None
    
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    elif context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
        except:
            await message.reply_text("❌ کاربر یافت نشد.")
            return
    else:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    if target_user.id in SUDO_USERS or db.is_sudo(target_user.id):
        await message.reply_text("❌ نمی‌توانید سودو را اخراج کنید!")
        return
    
    try:
        await chat.ban_member(target_user.id)
        await chat.unban_member(target_user.id)
        await message.reply_text(
            f"👢 {get_user_mention(target_user)} اخراج شد.",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

@group_only
@admin_only
async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اخطار دادن"""
    chat = update.effective_chat
    user = update.effective_user
    message = update.message
    target_user = None
    reason = "بدون دلیل"
    
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        if context.args:
            reason = ' '.join(context.args)
    elif context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
            if len(context.args) > 1:
                reason = ' '.join(context.args[1:])
        except:
            await message.reply_text("❌ کاربر یافت نشد.")
            return
    else:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    if target_user.id in SUDO_USERS or db.is_sudo(target_user.id):
        await message.reply_text("❌ نمی‌توانید به سودو اخطار دهید!")
        return
    
    db.add_group_member(chat.id, target_user.id)
    warns = db.add_warn(chat.id, target_user.id, reason)
    settings = db.get_group_settings(chat.id)
    max_warns = settings.get('max_warn', 3)
    
    if warns >= max_warns:
        action = settings.get('warn_action', 'mute')
        if action == 'ban':
            await chat.ban_member(target_user.id)
            action_text = "بن شد"
        elif action == 'kick':
            await chat.ban_member(target_user.id)
            await chat.unban_member(target_user.id)
            action_text = "اخراج شد"
        else:
            await chat.restrict_member(target_user.id, ChatPermissions(can_send_messages=False))
            action_text = "سکوت شد"
        db.reset_warns(chat.id, target_user.id)
        await message.reply_text(
            f"⚠️ {get_user_mention(target_user)} به حداکثر اخطار رسید و {action_text}!",
            parse_mode=ParseMode.HTML
        )
    else:
        await message.reply_text(
            f"⚡ {get_user_mention(target_user)} اخطار گرفت.\n📊 {warns}/{max_warns}\n📝 دلیل: {reason}",
            parse_mode=ParseMode.HTML
        )

@group_only
@admin_only
async def unwarn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف اخطار"""
    chat = update.effective_chat
    message = update.message
    target_user = message.reply_to_message.from_user if message.reply_to_message else None
    
    if not target_user and context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
        except:
            pass
    
    if not target_user:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    db.remove_warn(chat.id, target_user.id)
    warns, _ = db.get_warns(chat.id, target_user.id)
    await message.reply_text(
        f"✅ یک اخطار کم شد.\n📊 اخطار فعلی: {warns}",
        parse_mode=ParseMode.HTML
    )

@group_only
@admin_only
async def promote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ادمین کردن"""
    chat = update.effective_chat
    message = update.message
    target_user = message.reply_to_message.from_user if message.reply_to_message else None
    
    if not target_user and context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
        except:
            pass
    
    if not target_user:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    try:
        await chat.promote_member(
            target_user.id,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_invite_users=True
        )
        await message.reply_text(
            f"👑 {get_user_mention(target_user)} ادمین شد.",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

@group_only
@admin_only
async def demote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عزل ادمین"""
    chat = update.effective_chat
    message = update.message
    target_user = message.reply_to_message.from_user if message.reply_to_message else None
    
    if not target_user and context.args:
        try:
            target_user = (await context.bot.get_chat_member(chat.id, int(context.args[0]))).user
        except:
            pass
    
    if not target_user:
        await message.reply_text("❌ روی پیام ریپلای کنید.")
        return
    
    try:
        await chat.promote_member(
            target_user.id,
            can_delete_messages=False,
            can_restrict_members=False,
            can_pin_messages=False
        )
        await message.reply_text(
            f"📉 {get_user_mention(target_user)} عزل شد.",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ خطا: {e}")

# ==================== تنظیمات ====================

@group_only
@admin_only
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش تنظیمات"""
    settings = db.get_group_settings(update.effective_chat.id)
    await update.message.reply_text("⚙️ تنظیمات", reply_markup=Keyboards.settings_panel(settings))

@group_only
@admin_only
async def setwelcome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیم پیام خوش‌آمدگویی"""
    if not context.args:
        await update.message.reply_text(
            "📝 متن خوش‌آمد را بنویسید.\n\n"
            "متغیرها: {mention} {first_name} {group}"
        )
        return
    db.set_welcome_message(update.effective_chat.id, ' '.join(context.args))
    await update.message.reply_text("✅ پیام خوش‌آمد تنظیم شد.")

@group_only
@admin_only
async def setgoodbye_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیم پیام خداحافظی"""
    if not context.args:
        await update.message.reply_text("📝 متن خداحافظی را بنویسید.")
        return
    db.set_goodbye_message(update.effective_chat.id, ' '.join(context.args))
    await update.message.reply_text("✅ پیام خداحافظی تنظیم شد.")

@group_only
@admin_only
async def setrules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیم قوانین"""
    if not context.args:
        await update.message.reply_text("📝 قوانین را بنویسید.")
        return
    db.set_group_rules(update.effective_chat.id, ' '.join(context.args))
    await update.message.reply_text("✅ قوانین تنظیم شد.")

@group_only
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش قوانین"""
    rules = db.get_group_rules(update.effective_chat.id)
    if rules:
        await update.message.reply_text(f"📜 قوانین:\n\n{rules}")
    else:
        await update.message.reply_text("❌ قوانین تنظیم نشده.")

@group_only
@admin_only
async def lock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """قفل کردن"""
    if not context.args:
        await update.message.reply_text(
            "🔒 /lock [نوع]\n"
            "انواع: all, media, sticker, gif, voice, video, document, photo, url, forward"
        )
        return
    
    settings = db.get_group_settings(update.effective_chat.id)
    key = f"lock_{context.args[0].lower()}"
    
    if key in settings:
        settings[key] = True
        db.update_group_settings(update.effective_chat.id, settings)
        await update.message.reply_text(f"🔒 {context.args[0]} قفل شد.")
    else:
        await update.message.reply_text("❌ نوع نامعتبر.")

@group_only
@admin_only
async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """باز کردن قفل"""
    if not context.args:
        await update.message.reply_text("🔓 /unlock [نوع]")
        return
    
    settings = db.get_group_settings(update.effective_chat.id)
    key = f"lock_{context.args[0].lower()}"
    
    if key in settings:
        settings[key] = False
        db.update_group_settings(update.effective_chat.id, settings)
        await update.message.reply_text(f"🔓 {context.args[0]} باز شد.")

# ==================== بازی‌ها ====================

@group_only
async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست بازی‌ها"""
    await update.message.reply_text("🎮 بازی‌ها", reply_markup=Keyboards.games_panel())

@group_only
async def dice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بازی تاس"""
    result = roll_dice()
    emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"][result - 1]
    await update.message.reply_text(f"🎲 تاس: {emoji} ({result})")

@group_only
async def coin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بازی سکه"""
    await update.message.reply_text(f"🪙 سکه: {flip_coin()}")

@group_only
async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بازی کوییز"""
    question, answer, options = get_quiz()
    context.chat_data['quiz_answer'] = answer
    await update.message.reply_text(f"❓ {question}", reply_markup=Keyboards.captcha_keyboard(options))

@group_only
async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """سوال حقیقت"""
    await update.message.reply_text(f"💭 حقیقت:\n\n{get_truth()}")

@group_only
async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """چالش جرات"""
    await update.message.reply_text(f"🎯 جرات:\n\n{get_dare()}")

@group_only
async def riddle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معما"""
    question, answer = get_riddle()
    context.chat_data['riddle_answer'] = answer.lower()
    await update.message.reply_text(f"🧩 معما:\n\n{question}\n\n💡 جواب را بنویسید!")

# ==================== اقتصاد ====================

@group_only
async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش موجودی"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    eco = db.get_economy(chat_id, user_id)
    await update.message.reply_text(
        f"💰 موجودی شما:\n\n"
        f"🪙 کیف پول: {eco[3]:,} سکه\n"
        f"🏦 بانک: {eco[4]:,} سکه\n"
        f"📊 مجموع: {eco[3] + eco[4]:,} سکه"
    )

@group_only
async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاداش روزانه"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    eco = db.get_economy(chat_id, user_id)
    
    if eco[5]:
        last = datetime.fromisoformat(str(eco[5]))
        if (datetime.now() - last).total_seconds() < 86400:
            remaining = 86400 - (datetime.now() - last).total_seconds()
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            await update.message.reply_text(
                f"⏰ قبلاً پاداش روزانه گرفتید!\n"
                f"⏳ {hours} ساعت و {minutes} دقیقه مانده"
            )
            return
    
    reward = calculate_daily_reward()
    db.update_coins(chat_id, user_id, reward)
    db.set_daily_claimed(chat_id, user_id)
    await update.message.reply_text(f"🎁 پاداش روزانه: +{reward:,} سکه")
# ==================== CALLBACK ROUTER ====================

from telegram import Update
from telegram.ext import ContextTypes
from keyboards import Keyboards
from database import db

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat.id

    if data == "back_main":
        await query.message.edit_text(
            "🎛 پنل مدیریت گروه",
            reply_markup=Keyboards.main_panel()
        )

    elif data == "close_panel":
        await query.message.delete()

    elif data == "panel_members":
        await query.message.edit_text(
            "👥 پنل مدیریت اعضا",
            reply_markup=Keyboards.members_panel()
        )

    elif data == "panel_settings":
        settings = db.get_group_settings(chat_id)
        await query.message.edit_text(
            "⚙️ تنظیمات گروه",
            reply_markup=Keyboards.settings_panel(settings)
        )

    elif data == "panel_locks":
        settings = db.get_group_settings(chat_id)
        await query.message.edit_text(
            "🔒 قفل‌های گروه",
            reply_markup=Keyboards.locks_panel(settings)
        )

    elif data == "panel_security":
        settings = db.get_group_settings(chat_id)
        await query.message.edit_text(
            "🛡️ امنیت گروه",
            reply_markup=Keyboards.security_panel(settings)
        )

    elif data == "panel_games":
        await query.message.edit_text(
            "🎮 بازی‌ها",
            reply_markup=Keyboards.games_panel()
        )
