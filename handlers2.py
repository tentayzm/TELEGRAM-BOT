# handlers2.py - هندلرهای ربات (قسمت 2)

from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatMemberStatus
import random

from config import SUDO_USERS, TEXTS
from database import db
from keyboards import Keyboards
from utils import (
    get_user_mention, escape_html, format_welcome, format_stats_message,
    format_user_stats, format_leaderboard, calculate_daily_reward,
    calculate_work_reward, get_truth, get_dare, generate_captcha_math,
    contains_link, extract_links, is_whitelisted_link, check_bad_words
)

# ==================== ادامه اقتصاد ====================

async def daily_command_cont(update: Update, context: ContextTypes.DEFAULT_TYPE, eco, chat_id, user_id):
    """ادامه دستور روزانه"""
    if eco[5]:
        last = datetime.fromisoformat(str(eco[5]))
        if (datetime.now() - last).total_seconds() < 86400:
            remaining = 86400 - (datetime.now() - last).total_seconds()
            h, m = int(remaining // 3600), int((remaining % 3600) // 60)
            await update.message.reply_text(f"⏰ قبلاً گرفتید!\n⏳ {h} ساعت و {m} دقیقه مانده")
            return
    reward = calculate_daily_reward()
    db.update_coins(chat_id, user_id, reward)
    db.set_daily_claimed(chat_id, user_id)
    await update.message.reply_text(f"🎁 پاداش روزانه: +{reward:,} سکه")

async def work_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کار کردن"""
    chat_id, user_id = update.effective_chat.id, update.effective_user.id
    eco = db.get_economy(chat_id, user_id)
    
    if eco[7]:
        last = datetime.fromisoformat(str(eco[7]))
        if (datetime.now() - last).total_seconds() < 3600:
            remaining = 3600 - (datetime.now() - last).total_seconds()
            await update.message.reply_text(f"⏰ استراحت کنید!\n⏳ {int(remaining // 60)} دقیقه مانده")
            return
    
    job, reward = calculate_work_reward()
    db.update_coins(chat_id, user_id, reward)
    db.cursor.execute('UPDATE economy SET work_cooldown = ? WHERE chat_id = ? AND user_id = ?',
                     (datetime.now(), chat_id, user_id))
    db.conn.commit()
    await update.message.reply_text(f"💼 کار: {job}\n💰 +{reward:,} سکه")

async def transfer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """انتقال سکه"""
    chat_id, user_id = update.effective_chat.id, update.effective_user.id
    message = update.message
    
    if not message.reply_to_message or not context.args:
        await message.reply_text("💱 روی پیام ریپلای کنید و مبلغ بنویسید.")
        return
    
    try:
        amount = int(context.args[0])
    except:
        await message.reply_text("❌ مبلغ نامعتبر.")
        return
    
    if amount <= 0:
        await message.reply_text("❌ مبلغ باید مثبت باشد.")
        return
    
    target = message.reply_to_message.from_user
    if target.id == user_id:
        await message.reply_text("❌ نمی‌توانید به خود انتقال دهید!")
        return
    
    eco = db.get_economy(chat_id, user_id)
    if eco[3] < amount:
        await message.reply_text("❌ موجودی کافی نیست!")
        return
    
    db.transfer_coins(chat_id, user_id, target.id, amount)
    await message.reply_text(f"✅ {amount:,} سکه به {get_user_mention(target)} منتقل شد.", parse_mode=ParseMode.HTML)

# ==================== آمار ====================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """آمار گروه"""
    chat = update.effective_chat
    members = await chat.get_member_count()
    admins = len(await chat.get_administrators())
    stats = {'members': members, 'messages': db.get_group_members_count(chat.id), 'admins': admins, 'banned': 0, 'muted': 0}
    await update.message.reply_text(format_stats_message(stats), reply_markup=Keyboards.stats_panel())

async def mystats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """آمار من"""
    chat_id, user = update.effective_chat.id, update.effective_user
    db.add_group_member(chat_id, user.id)
    member = db.get_group_member(chat_id, user.id)
    data = {'messages': member[3], 'points': member[4], 'warns': member[5]} if member else {'messages': 0, 'points': 0, 'warns': 0}
    await update.message.reply_text(format_user_stats(data, user), parse_mode=ParseMode.HTML)

async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """برترین‌ها"""
    leaderboard = db.get_group_leaderboard(update.effective_chat.id, 10)
    await update.message.reply_text(format_leaderboard(leaderboard))

# ==================== نوت و فیلتر ====================

async def addnote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """افزودن نوت"""
    if len(context.args) < 2:
        await update.message.reply_text("📝 /addnote [نام] [محتوا]")
        return
    db.add_note(update.effective_chat.id, context.args[0], ' '.join(context.args[1:]), created_by=update.effective_user.id)
    await update.message.reply_text(f"✅ نوت '{context.args[0]}' ذخیره شد.")

async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش نوت"""
    chat_id = update.effective_chat.id
    if not context.args:
        notes = db.get_all_notes(chat_id)
        await update.message.reply_text("📋 نوت‌ها:\n" + '\n'.join([f"• {n[2]}" for n in notes]) if notes else "❌ نوتی نیست.")
        return
    note = db.get_note(chat_id, context.args[0])
    await update.message.reply_text(note[3] if note else f"❌ نوت '{context.args[0]}' یافت نشد.")

async def delnote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف نوت"""
    if not context.args:
        await update.message.reply_text("❌ نام نوت را بنویسید.")
        return
    db.remove_note(update.effective_chat.id, context.args[0])
    await update.message.reply_text(f"✅ نوت '{context.args[0]}' حذف شد.")

async def addfilter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """افزودن فیلتر"""
    if len(context.args) < 2:
        await update.message.reply_text("🔍 /addfilter [کلمه] [پاسخ]")
        return
    db.add_filter(update.effective_chat.id, context.args[0], ' '.join(context.args[1:]), created_by=update.effective_user.id)
    await update.message.reply_text(f"✅ فیلتر '{context.args[0]}' ذخیره شد.")

async def delfilter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف فیلتر"""
    if not context.args:
        await update.message.reply_text("❌ کلمه فیلتر را بنویسید.")
        return
    db.remove_filter(update.effective_chat.id, context.args[0])
    await update.message.reply_text(f"✅ فیلتر '{context.args[0]}' حذف شد.")

async def filters_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست فیلترها"""
    filters = db.get_all_filters(update.effective_chat.id)
    await update.message.reply_text("🔍 فیلترها:\n" + '\n'.join([f"• {f[2]}" for f in filters]) if filters else "❌ فیلتری نیست.")

# ==================== سودو ====================

async def addgroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """افزودن گروه مجاز"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    if not context.args:
        await update.message.reply_text("❌ آیدی گروه را وارد کنید.")
        return
    try:
        chat_id = int(context.args[0])
        db.add_allowed_group(chat_id, user_id)
        await update.message.reply_text(f"✅ گروه {chat_id} مجاز شد.")
    except:
        await update.message.reply_text("❌ آیدی نامعتبر.")

async def removegroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف گروه مجاز"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    if not context.args:
        await update.message.reply_text("❌ آیدی گروه را وارد کنید.")
        return
    try:
        db.remove_allowed_group(int(context.args[0]))
        await update.message.reply_text("✅ گروه حذف شد.")
    except:
        await update.message.reply_text("❌ آیدی نامعتبر.")

async def groups_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست گروه‌های مجاز"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    groups = db.get_allowed_groups()
    await update.message.reply_text("📋 گروه‌های مجاز:\n" + '\n'.join([f"• {g}" for g in groups]) if groups else "❌ گروهی نیست.")

async def addsudo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """افزودن سودو"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    if not context.args:
        await update.message.reply_text("❌ آیدی را وارد کنید.")
        return
    try:
        db.add_sudo(int(context.args[0]))
        await update.message.reply_text("✅ سودو اضافه شد.")
    except:
        await update.message.reply_text("❌ آیدی نامعتبر.")

async def removesudo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف سودو"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    if not context.args:
        await update.message.reply_text("❌ آیدی را وارد کنید.")
        return
    try:
        db.remove_sudo(int(context.args[0]))
        await update.message.reply_text("✅ سودو حذف شد.")
    except:
        await update.message.reply_text("❌ آیدی نامعتبر.")

async def sudos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست سودوها"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    sudos = db.get_sudos()
    text = "👑 سودوها:\n" + '\n'.join([f"• {s} (اصلی)" for s in SUDO_USERS])
    text += '\n'.join([f"• {s}" for s in sudos if s not in SUDO_USERS])
    await update.message.reply_text(text)

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام همگانی"""
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS and not db.is_sudo(user_id):
        await update.message.reply_text("❌ فقط سودو.")
        return
    if not context.args:
        await update.message.reply_text("❌ متن را بنویسید.")
        return
    
    text = ' '.join(context.args)
    groups = db.get_all_groups()
    success, failed = 0, 0
    
    for g in groups:
        try:
            await context.bot.send_message(g[0], text)
            success += 1
        except:
            failed += 1
    
    await update.message.reply_text(f"📢 ارسال شد!\n✅ {success}\n❌ {failed}")

# ==================== رویدادها ====================

async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عضو جدید"""
    chat = update.effective_chat
    
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            adder = update.effective_user
            if adder.id not in SUDO_USERS and not db.is_sudo(adder.id):
                await update.message.reply_text("❌ فقط سودو می‌تواند ربات را اضافه کند!")
                await chat.leave()
                return
            else:
                db.add_allowed_group(chat.id, adder.id)
                db.add_group(chat.id, chat.title, chat.username, adder.id)
                await update.message.reply_text("✅ ربات فعال شد!\n/panel برای پنل مدیریت")
            return
    
    if not db.is_allowed_group(chat.id):
        return
    
    settings = db.get_group_settings(chat.id)
    
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
        
        db.add_user(member.id, member.username, member.first_name, member.last_name)
        db.add_group_member(chat.id, member.id)
        
        if settings.get('welcome_enabled', True):
            welcome = db.get_welcome_message(chat.id) or TEXTS['fa']['welcome']
            text = format_welcome(welcome, member, chat)
            
            if settings.get('captcha_enabled', False):
                question, answer, options = generate_captcha_math()
                context.chat_data[f'captcha_{member.id}'] = answer
                await update.message.reply_text(f"{text}\n\n🔐 کپچا:\n{question}", reply_markup=Keyboards.captcha_keyboard(options), parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def left_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """خروج عضو"""
    chat = update.effective_chat
    member = update.message.left_chat_member
    
    if member.id == context.bot.id:
        db.remove_allowed_group(chat.id)
        return
    
    if not db.is_allowed_group(chat.id):
        return
    
    settings = db.get_group_settings(chat.id)
    if settings.get('goodbye_enabled', True):
        goodbye = db.get_goodbye_message(chat.id) or TEXTS['fa']['goodbye']
        await update.message.reply_text(format_welcome(goodbye, member, chat), parse_mode=ParseMode.HTML)

# ==================== پیام ====================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر پیام‌ها"""
    if not update.message or not update.effective_chat:
        return
    
    chat = update.effective_chat
    user = update.effective_user
    message = update.message
    
    if chat.type not in ['group', 'supergroup']:
        return
    
    if not db.is_allowed_group(chat.id):
        return
    
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.add_group_member(chat.id, user.id)
    db.update_member_messages(chat.id, user.id)
    
    if message.text:
        # فیلترها
        for f in db.get_all_filters(chat.id):
            if f[2].lower() in message.text.lower():
                await message.reply_text(f[3])
                break
        
        # معما
        if 'riddle_answer' in context.chat_data:
            if message.text.lower() == context.chat_data['riddle_answer']:
                del context.chat_data['riddle_answer']
                db.update_member_points(chat.id, user.id, 10)
                await message.reply_text(f"✅ درست! {get_user_mention(user)} +10 امتیاز", parse_mode=ParseMode.HTML)
    
    settings = db.get_group_settings(chat.id)
    
    # آنتی‌لینک
    if settings.get('antilink_enabled') and message.text:
        if user.id not in SUDO_USERS and not db.is_sudo(user.id):
            member = await chat.get_member(user.id)
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                if contains_link(message.text):
                    whitelist = db.get_whitelist_links(chat.id)
                    for link in extract_links(message.text):
                        if not is_whitelisted_link(link, whitelist):
                            await message.delete()
                            await context.bot.send_message(chat.id, f"🔗 لینک {get_user_mention(user)} حذف شد.", parse_mode=ParseMode.HTML)
                            return
    
    # کلمات ممنوعه
    if message.text:
        word, action = check_bad_words(message.text, db.get_banned_words(chat.id))
        if word:
            await message.delete()
            if action == 'warn':
                db.add_warn(chat.id, user.id, f"کلمه ممنوعه: {word}")
            await context.bot.send_message(chat.id, f"⚠️ پیام {get_user_mention(user)} حذف شد.", parse_mode=ParseMode.HTML)

# ==================== کالبک ====================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر کالبک"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat = update.effective_chat
    user = update.effective_user
    
    if data == "close_panel":
        await query.message.delete()
        return
    
    if data == "back_main":
        await query.message.edit_text("🎛 پنل مدیریت", reply_markup=Keyboards.main_panel())
        return
    
    # پنل‌ها
    panels = {
        "panel_members": ("👥 مدیریت اعضا", Keyboards.members_panel()),
        "panel_games": ("🎮 بازی‌ها", Keyboards.games_panel()),
        "panel_economy": ("💰 اقتصاد", Keyboards.economy_panel()),
        "panel_stats": ("📊 آمار", Keyboards.stats_panel()),
        "panel_tools": ("🎯 ابزارها", Keyboards.tools_panel()),
        "panel_notes": ("📋 نوت و فیلتر", Keyboards.notes_panel()),
        "panel_giveaway": ("🎁 قرعه‌کشی", Keyboards.giveaway_panel()),
        "panel_events": ("📅 رویدادها", Keyboards.events_panel()),
        "panel_messages": ("📝 پیام‌ها", Keyboards.messages_panel()),
    }
    
    if data in panels:
        await query.message.edit_text(panels[data][0], reply_markup=panels[data][1])
        return
    
    if data == "panel_settings":
        settings = db.get_group_settings(chat.id)
        await query.message.edit_text("⚙️ تنظیمات", reply_markup=Keyboards.settings_panel(settings))
        return
    
    if data == "panel_locks":
        settings = db.get_group_settings(chat.id)
        await query.message.edit_text("🔒 قفل‌ها", reply_markup=Keyboards.locks_panel(settings))
        return
    
    if data == "panel_security":
        settings = db.get_group_settings(chat.id)
        await query.message.edit_text("🛡️ امنیت", reply_markup=Keyboards.security_panel(settings))
        return
    
    # تغییر تنظیمات
    if data.startswith("toggle_"):
        setting = data.replace("toggle_", "")
        settings = db.get_group_settings(chat.id)
        settings[setting] = not settings.get(setting, False)
        db.update_group_settings(chat.id, settings)
        
        if "lock" in setting:
            await query.message.edit_reply_markup(Keyboards.locks_panel(settings))
        elif "anti" in setting:
            await query.message.edit_reply_markup(Keyboards.security_panel(settings))
        else:
            await query.message.edit_reply_markup(Keyboards.settings_panel(settings))
        return
    
    # کپچا
    if data.startswith("captcha_"):
        answer = data.replace("captcha_", "")
        correct = context.chat_data.get(f'captcha_{user.id}')
        if correct and str(answer) == str(correct):
            del context.chat_data[f'captcha_{user.id}']
            db.set_captcha_verified(chat.id, user.id, True)
            await query.message.edit_text("✅ کپچا تأیید شد!")
        else:
            await query.answer("❌ اشتباه!", show_alert=True)
        return
    
    # بازی‌ها
    if data == "game_dice":
        from utils import roll_dice
        result = roll_dice()
        emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"][result - 1]
        await query.message.reply_text(f"🎲 {get_user_mention(user)}: {emoji} ({result})", parse_mode=ParseMode.HTML)
    
    elif data == "game_coin":
        from utils import flip_coin
        await query.message.reply_text(f"🪙 {get_user_mention(user)}: {flip_coin()}", parse_mode=ParseMode.HTML)
    
    elif data == "game_truth_dare":
        await query.message.edit_text("🎭 حقیقت یا جرات", reply_markup=Keyboards.truth_dare_keyboard())
    
    elif data == "td_truth":
        await query.message.reply_text(f"💭 {get_user_mention(user)}:\n\n{get_truth()}", parse_mode=ParseMode.HTML)
    
    elif data == "td_dare":
        await query.message.reply_text(f"🎯 {get_user_mention(user)}:\n\n{get_dare()}", parse_mode=ParseMode.HTML)
    
    elif data == "td_random":
        if random.choice([True, False]):
            await query.message.reply_text(f"💭 {get_user_mention(user)}:\n\n{get_truth()}", parse_mode=ParseMode.HTML)
        else:
            await query.message.reply_text(f"🎯 {get_user_mention(user)}:\n\n{get_dare()}", parse_mode=ParseMode.HTML)
    
    # اقتصاد
    elif data == "eco_balance":
        eco = db.get_economy(chat.id, user.id)
        await query.message.reply_text(f"💰 {get_user_mention(user)}:\n🪙 {eco[3]:,}\n🏦 {eco[4]:,}", parse_mode=ParseMode.HTML)
    
    elif data == "eco_daily":
        eco = db.get_economy(chat.id, user.id)
        if eco[5]:
            last = datetime.fromisoformat(str(eco[5]))
            if (datetime.now() - last).total_seconds() < 86400:
                await query.answer("⏰ قبلاً گرفتید!", show_alert=True)
                return
        reward = calculate_daily_reward()
        db.update_coins(chat.id, user.id, reward)
        db.set_daily_claimed(chat.id, user.id)
        await query.message.reply_text(f"🎁 {get_user_mention(user)}: +{reward:,}", parse_mode=ParseMode.HTML)
    
    elif data == "eco_richest":
        richest = db.get_richest(chat.id, 10)
        medals = ["🥇", "🥈", "🥉"]
        text = "🏆 ثروتمندترین‌ها:\n\n"
        for i, (uid, total) in enumerate(richest, 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            text += f"{medal} {uid}: {total:,}\n"
        await query.message.reply_text(text)
    
    # آمار
    elif data == "stats_me":
        db.add_group_member(chat.id, user.id)
        member = db.get_group_member(chat.id, user.id)
        data = {'messages': member[3], 'points': member[4], 'warns': member[5]} if member else {'messages': 0, 'points': 0, 'warns': 0}
        await query.message.reply_text(format_user_stats(data, user), parse_mode=ParseMode.HTML)
    
    elif data == "stats_top":
        await query.message.reply_text(format_leaderboard(db.get_group_leaderboard(chat.id, 10)))
    
    # هدرها
    elif data in ["h", "h2", "h3", "f", "header", "footer", "page_info"]:
        pass
    
    elif data == "cancel":
        await query.message.delete()
