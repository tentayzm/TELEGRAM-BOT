# utils.py - توابع کمکی

import re
import random
import string
from datetime import datetime, timedelta
from config import RANKS, EMOJIS

# ==================== توابع زمان ====================

def parse_time(time_str):
    """تبدیل رشته زمان به ثانیه"""
    time_str = time_str.lower().strip()
    
    patterns = {
        r'^(\d+)s$': 1,           # ثانیه
        r'^(\d+)m$': 60,          # دقیقه
        r'^(\d+)h$': 3600,        # ساعت
        r'^(\d+)d$': 86400,       # روز
        r'^(\d+)w$': 604800,      # هفته
    }
    
    for pattern, multiplier in patterns.items():
        match = re.match(pattern, time_str)
        if match:
            return int(match.group(1)) * multiplier
    
    return None

def format_time(seconds):
    """تبدیل ثانیه به رشته خوانا"""
    if seconds is None or seconds == 0:
        return "همیشگی"
    
    intervals = [
        ('هفته', 604800),
        ('روز', 86400),
        ('ساعت', 3600),
        ('دقیقه', 60),
        ('ثانیه', 1),
    ]
    
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")
    
    return ' و '.join(result) if result else "0 ثانیه"

def format_datetime(dt):
    """فرمت کردن تاریخ و زمان"""
    if dt is None:
        return "نامشخص"
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime("%Y/%m/%d - %H:%M")

def time_ago(dt):
    """محاسبه زمان گذشته"""
    if dt is None:
        return "نامشخص"
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    
    diff = datetime.now() - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "همین الان"
    elif seconds < 3600:
        return f"{int(seconds // 60)} دقیقه پیش"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} ساعت پیش"
    elif seconds < 604800:
        return f"{int(seconds // 86400)} روز پیش"
    else:
        return format_datetime(dt)

# ==================== توابع کاربر ====================

def get_user_mention(user):
    """ایجاد منشن کاربر"""
    if hasattr(user, 'id'):
        name = user.first_name or "کاربر"
        return f'<a href="tg://user?id={user.id}">{name}</a>'
    return "کاربر"

def get_user_link(user_id, name="کاربر"):
    """ایجاد لینک کاربر"""
    return f'<a href="tg://user?id={user_id}">{name}</a>'

def get_user_rank(messages):
    """دریافت رتبه کاربر بر اساس پیام"""
    rank_name = "🐣 تازه‌کار"
    for threshold, (name, _) in sorted(RANKS.items(), reverse=True):
        if messages >= threshold:
            rank_name = name
            break
    return rank_name

def get_next_rank(messages):
    """دریافت رتبه بعدی و پیام‌های مورد نیاز"""
    for threshold in sorted(RANKS.keys()):
        if messages < threshold:
            return RANKS[threshold][0], threshold - messages
    return None, 0

# ==================== توابع امنیتی ====================

def contains_link(text):
    """بررسی وجود لینک در متن"""
    patterns = [
        r'https?://[^\s]+',
        r'www\.[^\s]+',
        r't\.me/[^\s]+',
        r'telegram\.me/[^\s]+',
        r'@[a-zA-Z0-9_]+',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def extract_links(text):
    """استخراج لینک‌ها از متن"""
    pattern = r'(https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+)'
    return re.findall(pattern, text, re.IGNORECASE)

def contains_arabic(text):
    """بررسی وجود حروف عربی"""
    arabic_pattern = re.compile('[\u0600-\u06FF]')
    return bool(arabic_pattern.search(text))

def contains_english(text):
    """بررسی وجود حروف انگلیسی"""
    return bool(re.search('[a-zA-Z]', text))

def contains_emoji(text):
    """بررسی وجود ایموجی"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

def contains_mention(text):
    """بررسی وجود منشن"""
    return bool(re.search(r'@[a-zA-Z0-9_]+', text))

def contains_hashtag(text):
    """بررسی وجود هشتگ"""
    return bool(re.search(r'#[^\s]+', text))

def contains_forward(message):
    """بررسی فوروارد بودن پیام"""
    return message.forward_date is not None

def is_admin_command(text):
    """بررسی دستور ادمین بودن"""
    admin_commands = [
        '/ban', '/unban', '/mute', '/unmute', '/kick',
        '/warn', '/unwarn', '/promote', '/demote',
        '/lock', '/unlock', '/purge', '/pin', '/unpin'
    ]
    return any(text.startswith(cmd) for cmd in admin_commands)

def is_spam(text, max_repeats=5):
    """بررسی اسپم بودن"""
    # بررسی تکرار کاراکتر
    for char in set(text):
        if text.count(char * max_repeats) > 0:
            return True
    
    # بررسی تکرار کلمه
    words = text.split()
    if len(words) > 3:
        for word in set(words):
            if words.count(word) > max_repeats:
                return True
    
    return False

def is_flood(messages_times, limit=5, time_window=10):
    """بررسی فلود بودن"""
    if len(messages_times) < limit:
        return False
    
    now = datetime.now()
    recent = [t for t in messages_times if (now - t).total_seconds() <= time_window]
    return len(recent) >= limit

def check_bad_words(text, bad_words):
    """بررسی کلمات ممنوعه"""
    text_lower = text.lower()
    for word, action in bad_words:
        if word.lower() in text_lower:
            return word, action
    return None, None

def is_whitelisted_link(link, whitelist):
    """بررسی لینک در لیست سفید"""
    for white_link in whitelist:
        if white_link.lower() in link.lower():
            return True
    return False

# ==================== توابع متن ====================

def escape_html(text):
    """اسکیپ کردن HTML"""
    if text is None:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def truncate_text(text, max_length=100):
    """کوتاه کردن متن"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def format_number(num):
    """فرمت کردن اعداد"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    return str(num)

def generate_random_string(length=8):
    """تولید رشته تصادفی"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_captcha_math():
    """تولید کپچا ریاضی"""
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(['+', '-', '*'])
    
    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2
    
    question = f"{num1} {operation} {num2} = ?"
    
    # گزینه‌های اشتباه
    options = [answer]
    while len(options) < 4:
        wrong = answer + random.randint(-5, 5)
        if wrong != answer and wrong not in options:
            options.append(wrong)
    
    random.shuffle(options)
    return question, answer, options

def generate_captcha_text(length=4):
    """تولید کپچا متنی"""
    chars = string.ascii_uppercase + string.digits
    captcha = ''.join(random.choices(chars, k=length))
    return captcha

# ==================== توابع بازی ====================

def get_random_number(min_val=1, max_val=100):
    """تولید عدد تصادفی"""
    return random.randint(min_val, max_val)

def get_random_word():
    """انتخاب کلمه تصادفی"""
    words = [
        "سیب", "موز", "پرتقال", "هندوانه", "انگور",
        "گربه", "سگ", "پرنده", "ماهی", "فیل",
        "خانه", "مدرسه", "کتاب", "قلم", "میز",
        "آفتاب", "ماه", "ستاره", "آسمان", "زمین",
        "درخت", "گل", "برگ", "آب", "آتش",
        "کوه", "دریا", "رودخانه", "جنگل", "صحرا"
    ]
    return random.choice(words)

def roll_dice():
    """تاس انداختن"""
    return random.randint(1, 6)

def flip_coin():
    """سکه انداختن"""
    return random.choice(["شیر", "خط"])

def rock_paper_scissors(choice):
    """سنگ کاغذ قیچی"""
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    
    if choice == bot_choice:
        return bot_choice, "draw"
    
    wins = {
        ("rock", "scissors"): True,
        ("scissors", "paper"): True,
        ("paper", "rock"): True,
    }
    
    if (choice, bot_choice) in wins:
        return bot_choice, "win"
    return bot_choice, "lose"

def get_truth():
    """سوال حقیقت"""
    truths = [
        "آخرین باری که دروغ گفتی چه زمانی بود؟",
        "بزرگترین ترست چیست؟",
        "اگه یه سوپرپاور داشتی چی می‌خواستی؟",
        "بهترین خاطره‌ات چیست؟",
        "بدترین عادتت چیست؟",
        "اگه فقط یه غذا می‌تونستی تا آخر عمر بخوری چی بود؟",
        "از چه چیزی بیشتر از همه پشیمونی؟",
        "بهترین دوستت کیه؟",
        "آخرین بار که گریه کردی کی بود؟",
        "اگه لاتاری ببری چیکار میکنی؟",
        "بزرگترین رازت چیست؟",
        "از چه کسی متنفری؟",
        "اولین عشقت کی بود؟",
        "بدترین خاطره‌ات چیست؟",
        "اگه یه روز زندگیت باقی مونده بود چیکار میکردی؟"
    ]
    return random.choice(truths)

def get_dare():
    """چالش جرات"""
    dares = [
        "یه جوک تعریف کن!",
        "یه آهنگ بخون!",
        "یه شعر بگو!",
        "یه ایموجی بفرست که حالتو نشون بده!",
        "یه عکس از خودت بفرست!",
        "یه ویس بفرست!",
        "به نفر بعدی یه تعریف کن!",
        "یه راز درباره خودت بگو!",
        "یه کلمه به زبان دیگه یاد بده!",
        "یه نقاشی بکش و بفرست!",
        "30 ثانیه هیچی نگو!",
        "یه استیکر خنده‌دار بفرست!",
        "یه پیام به آخرین کسی که باهاش چت کردی بفرست!",
        "پروفایلتو عوض کن!",
        "یه متن طولانی تایپ کن!"
    ]
    return random.choice(dares)

def get_riddle():
    """معما"""
    riddles = [
        ("چه چیزی پا نداره ولی راه میره؟", "ساعت"),
        ("چه چیزی هرچی بیشتر ازش برداری بزرگتر میشه؟", "چاله"),
        ("چه چیزی سر نداره ولی کلاه داره؟", "قارچ"),
        ("چه چیزی همه جا میره ولی از جاش تکون نمیخوره؟", "جاده"),
        ("چه چیزی دهن داره ولی حرف نمیزنه؟", "رودخانه"),
        ("چه چیزی گوش داره ولی نمیشنوه؟", "کوزه"),
        ("چه چیزی چشم داره ولی نمیبینه؟", "سوزن"),
        ("چه چیزی دست داره ولی نمیگیره؟", "ساعت"),
        ("چه چیزی پر میشه ولی خالی نمیشه؟", "سال"),
        ("چه چیزی سیاهه ولی روشنایی میده؟", "ذغال")
    ]
    return random.choice(riddles)

def get_quiz():
    """سوال کوییز"""
    quizzes = [
        ("پایتخت ایران کجاست؟", "تهران", ["اصفهان", "شیراز", "مشهد"]),
        ("بزرگترین سیاره منظومه شمسی چیست؟", "مشتری", ["زحل", "زمین", "مریخ"]),
        ("سریعترین حیوان جهان چیست؟", "یوزپلنگ", ["شیر", "عقاب", "خرگوش"]),
        ("بلندترین کوه جهان چیست؟", "اورست", ["کی۲", "کلیمانجارو", "دماوند"]),
        ("بزرگترین اقیانوس جهان چیست؟", "آرام", ["اطلس", "هند", "منجمد شمالی"]),
        ("چند قاره در جهان وجود دارد؟", "۷", ["۵", "۶", "۸"]),
        ("زبان رسمی برزیل چیست؟", "پرتغالی", ["اسپانیایی", "انگلیسی", "فرانسوی"]),
        ("نماد شیمیایی طلا چیست؟", "Au", ["Ag", "Fe", "Cu"]),
        ("کدام سیاره به سیاره سرخ معروف است؟", "مریخ", ["مشتری", "زهره", "عطارد"]),
        ("قلب انسان چند حفره دارد؟", "۴", ["۲", "۳", "۵"])
    ]
    q = random.choice(quizzes)
    options = [q[1]] + q[2]
    random.shuffle(options)
    return q[0], q[1], options

# ==================== توابع اقتصادی ====================

def calculate_daily_reward(streak=1):
    """محاسبه پاداش روزانه"""
    base_reward = 100
    streak_bonus = min(streak * 10, 100)
    return base_reward + streak_bonus

def calculate_work_reward():
    """محاسبه پاداش کار"""
    jobs = [
        ("برنامه‌نویس", (50, 150)),
        ("معلم", (40, 120)),
        ("دکتر", (60, 180)),
        ("راننده", (30, 100)),
        ("آشپز", (35, 110)),
        ("نویسنده", (45, 130)),
        ("هنرمند", (40, 140)),
        ("مهندس", (55, 160)),
    ]
    job = random.choice(jobs)
    reward = random.randint(job[1][0], job[1][1])
    return job[0], reward

def gamble(amount, win_chance=0.45):
    """قمار"""
    if random.random() < win_chance:
        return int(amount * 2), True
    return 0, False

# ==================== توابع فرمت پیام ====================

def format_welcome(template, user, chat):
    """فرمت کردن پیام خوش‌آمدگویی"""
    replacements = {
        "{mention}": get_user_mention(user),
        "{first_name}": escape_html(user.first_name or ""),
        "{last_name}": escape_html(user.last_name or ""),
        "{full_name}": escape_html(f"{user.first_name or ''} {user.last_name or ''}".strip()),
        "{username}": f"@{user.username}" if user.username else "بدون یوزرنیم",
        "{user_id}": str(user.id),
        "{group}": escape_html(chat.title or "گروه"),
        "{chat_id}": str(chat.id),
    }
    
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    
    return result

def format_stats_message(stats):
    """فرمت کردن پیام آمار"""
    message = f"""
╔════════════════════════════╗
║         📊 آمار گروه         ║
╠════════════════════════════╣
║ 👥 اعضا: {stats.get('members', 0):,}
║ 📝 پیام‌ها: {stats.get('messages', 0):,}
║ 👑 ادمین‌ها: {stats.get('admins', 0)}
║ 🚫 بن‌شده‌ها: {stats.get('banned', 0)}
║ 🔇 سکوت‌شده‌ها: {stats.get('muted', 0)}
╚════════════════════════════╝
"""
    return message

def format_user_stats(user_data, user):
    """فرمت کردن آمار کاربر"""
    rank = get_user_rank(user_data.get('messages', 0))
    next_rank, needed = get_next_rank(user_data.get('messages', 0))
    
    message = f"""
╔════════════════════════════╗
║       👤 آمار کاربر        ║
╠════════════════════════════╣
║ 👤 نام: {escape_html(user.first_name or 'نامشخص')}
║ 📝 پیام‌ها: {user_data.get('messages', 0):,}
║ ⭐ امتیاز: {user_data.get('points', 0):,}
║ 🏆 رتبه: {rank}
║ ⚡ اخطارها: {user_data.get('warns', 0)}
"""
    
    if next_rank:
        message += f"║ 📈 رتبه بعدی: {next_rank} ({needed} پیام مانده)\n"
    
    message += "╚════════════════════════════╝"
    return message

def format_leaderboard(leaderboard, title="🏆 برترین‌ها"):
    """فرمت کردن لیدربورد"""
    medals = ["🥇", "🥈", "🥉"]
    
    message = f"""
╔════════════════════════════╗
║         {title}         ║
╠════════════════════════════╣
"""
    
    for i, (user_id, messages, points) in enumerate(leaderboard[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        message += f"║ {medal} کاربر {user_id}: {messages:,} پیام\n"
    
    message += "╚════════════════════════════╝"
    return message
