#ADMIN_ID = 6128719325
#TOKEN = "8571268911:AAFA8GbVk6dCDbWWQ2L_8hy7o6aPT3DsPs0"

#ADMIN_ID = 6128719325
#TOKEN = "8551890851:AAF-HJCylKAw6rq6wEdZAUdJ3aYllRuFjz4"
from aiogram.exceptions import TelegramBadRequest

import random
import string
import time
import asyncio
import sqlite3
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from aiogram import F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

async def safe_answer(callback: CallbackQuery):
    try:
        await  safe_answer(callback)
    except:
        pass


class RejectFSM(StatesGroup):
    typing_reason = State()

LOG_CHANNEL_ID = -1003552303944
MIN_WITHDRAW_STARS = 100
ADMIN_ID = 6128719325
TOKEN = "8551890851:AAF-HJCylKAw6rq6wEdZAUdJ3aYllRuFjz4"
from aiogram import Bot

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

OPEN_CHANNELS = {
    "@prosadin": "Подписаться на @prosadin"
}

CS_SKINS = {
    "ak_redline": ("AK-47 | Redline", 350),
    "awp_asiimov": ("AWP | Asiimov", 900),
    "m4_howl": ("M4A4 | Howl", 1200),
    "usp_kill": ("USP-S | Kill Confirmed", 500),
    "glock_fade": ("Glock-18 | Fade", 650),
    "deagle_blaze": ("Desert Eagle | Blaze", 700),
    "knife_bayo": ("Bayonet | Doppler", 2000),
    "knife_karambit": ("Karambit | Tiger Tooth", 2500),
    "ak_fire": ("AK-47 | Fire Serpent", 1800),
    "m4_print": ("M4A1-S | Printstream", 1100),
}

GIFT_EMOJIS = {
    "15a": "🧸",
    "15b": "💝",
    "25a": "🌹",
    "25b": "🎁",
    "50a": "🎂",
    "50b": "🏆",
    "50c": "💐",
    "50d": "🍾",
    "100a": "💍",
    "100b": "💎",
    "dog_snoop": "🐶",
    "packet": "🌿",
    "box": "🗃️",
    "swords": "⚔🌌",
    "candle": "🕯",
    "mushroom": "🍄",
    "new_nft": "👑",
    "dogs9999": "🐾",
    "lostdogs": "🐕"
}

GIFT_STAR_COST = {
    "15a": 15,
    "15b": 15,
    "25a": 25,
    "25b": 25,
    "50a": 50,
    "50b": 50,
    "50c": 50,
    "50d": 50,
    "100a": 100,
    "100b": 100,
}

NFT_GIFTS = {
    "dog_snoop": ("Собака снупдога", 500),
    "packet": ("Пакетик", 550),
    "box": ("Шкатулка", 500),
    "swords": ("Мечи", 200),
    "candle": ("Свечка", 1000),
    "mushroom": ("Гриб", 777),
    "new_nft": ("Новые NFT подарки", 0),  # кнопка для раздела новых NFT (если нужно, можно обработать отдельно)
}

GIFT_CATALOG = {
    "15a": "🧸 Мишка",
    "15b": "💝 Сердце",
    "25a": "🌹 Роза",
    "25b": "🎁 Сюрприз",
    "50a": "🎂 Торт",
    "50b": "🏆 Кубок",
    "50c": "💐 Букет",
    "50d": "🍾 Шампанское",
    "100a": "💍 Кольцо",
    "100b": "💎 Алмаз",

    # NFT / спец
    "dog_snoop": "🐶 Собака Snoop",
    "packet": "🌿 Пакетик",
    "box": "🗃 Шкатулка",
    "swords": "⚔🌌 Мечи",
    "candle": "🕯 Свеча",
    "mushroom": "🍄 Гриб",
}

# 💰 стоимость подарков для реферального бонуса
GIFT_PRICES = {
    "15a": 15,
    "15b": 15,
    "25a": 25,
    "25b": 25,
    "50a": 50,
    "50b": 50,
    "50c": 50,
    "50d": 50,
    "100a": 100,
    "100b": 100,

    # если есть NFT
    "dog_snoop": 500,
    "packet": 550,
    "box": 500,
    "swords": 200,
    "candle": 1000,
    "mushroom": 777,
}



def gift_name(code: str) -> str:
    return GIFT_CATALOG.get(code, code)


class RejectReason(StatesGroup):
    waiting_for_reason = State()


# --- SQLite setup ---
conn = sqlite3.connect("database2.db", check_same_thread=False)
cursor = conn.cursor()

# --- users ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_surname TEXT,
    username TEXT,
    referrer_id INTEGER,
    stars INTEGER DEFAULT 0,
    selected_gift TEXT,
    free_exchange_used INTEGER DEFAULT 0,
    rules_accepted INTEGER DEFAULT 0,
    last_checkin INTEGER DEFAULT 0
)
""")
# --- nickname bonus migration ---

conn.commit()

# --- star transactions ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS star_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    type TEXT,              -- bonus | withdraw | exchange | referral | checkin
    description TEXT,
    created_at INTEGER
)
""")
conn.commit()

# --- withdrawals ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,              -- stars | gift
    amount INTEGER,
    gift_code TEXT,
    status TEXT DEFAULT 'pending',
    created_at INTEGER
)
""")
conn.commit()


# --- vouchers ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS vouchers (
    code TEXT PRIMARY KEY,
    stars INTEGER NOT NULL,
    max_uses INTEGER NOT NULL,
    per_user_limit INTEGER NOT NULL,
    used_count INTEGER DEFAULT 0,
    created_at INTEGER
)
""")

# --- voucher uses ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS voucher_uses (
    code TEXT,
    user_id INTEGER,
    used_at INTEGER,
    PRIMARY KEY (code, user_id)
)
""")

conn.commit()

# --- user gifts ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_gifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    gift_code TEXT,
    status TEXT DEFAULT 'pending',   -- pending | requested | delivered
    created_at INTEGER
)
""")
conn.commit()
# --- nickname bonus migration ---


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return column_name in [row[1] for row in cursor.fetchall()]


if not column_exists(cursor, "users", "nickname_bonus_last"):
    cursor.execute("ALTER TABLE users ADD COLUMN nickname_bonus_last INTEGER DEFAULT 0")

if not column_exists(cursor, "users", "nickname_bonus_blocked_until"):
    cursor.execute("ALTER TABLE users ADD COLUMN nickname_bonus_blocked_until INTEGER DEFAULT 0")


# --- migrations ---
try:
    if not column_exists(cursor, "withdrawals", "gift_id"):
        cursor.execute("ALTER TABLE withdrawals ADD COLUMN gift_id INTEGER")

    conn.commit()
except Exception as e:
    print("DB migration error:", e)


def build_exchange_main_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    accepted = has_accepted_rules(user_id)

    builder.row(
        InlineKeyboardButton(text="🎁 Основные подарки", callback_data="exchange_regular"),
        InlineKeyboardButton(
            text=("🖼 NFT подарки" if accepted else "🔒 NFT подарки"),
            callback_data=("exchange_nft" if accepted else "locked")
        )
    )
    builder.row(
        InlineKeyboardButton(text="💎 Бонус за ник", callback_data="nickname_bonus")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Лидерборд", callback_data="leaderboard")
    )

    builder.row(
        InlineKeyboardButton(
            text=("🖌 Стикеры" if accepted else "🔒 Стикеры"),
            callback_data=("exchange_stickers" if accepted else "locked")
        ),
        InlineKeyboardButton(
            text=("🎮 Скины CS2" if accepted else "🔒 Скины CS2"),
            callback_data=("exchange_cs" if accepted else "locked")
        )
    )

    builder.row(
        InlineKeyboardButton(text="📅 Ежедневный чек-ин", callback_data="daily_checkin")
    )

    builder.row(
        InlineKeyboardButton(text="📦 Мои подарки / ⭐ Вывод", callback_data="my_withdraw")
    )

    builder.row(
        InlineKeyboardButton(text="⭐ Баланс", callback_data="my_balance")
    )

    builder.row(
        InlineKeyboardButton(text="🎟 Активировать ваучер", callback_data="voucher_info")
    )

    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_after_ok")
    )

    return builder.as_markup()
def build_exchange_cs_keyboard():
    builder = InlineKeyboardBuilder()

    for key, (name, cost) in CS_SKINS.items():
        builder.row(
            InlineKeyboardButton(
                text=f"🎮 {name} — ⭐{cost}",
                callback_data=f"exchange_cs_{key}"
            )
        )

    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")
    )

    return builder.as_markup()
@dp.callback_query(F.data == "exchange_cs")
async def exchange_cs_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎮 <b>Скины CS2</b>\n\nВыберите скин для обмена:",
        reply_markup=build_exchange_cs_keyboard()
    )


@dp.callback_query(F.data == "daily_checkin")
async def daily_checkin(callback: CallbackQuery):
    user_id = callback.from_user.id
    now = int(time.time())

    cursor.execute("SELECT last_checkin FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    last_checkin = result[0] if result else 0

    # 24 часа = 86400 секунд
    if now - last_checkin < 86400:
        remaining = 86400 - (now - last_checkin)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        await callback.answer(
            f"⏳ Чек-ин уже был!\nПопробуй через {hours}ч {minutes}м",
            show_alert=True
        )
        return

    # награда
    reward = 10
    add_stars(user_id, reward)

    cursor.execute(
        "UPDATE users SET last_checkin = ? WHERE user_id = ?",
        (now, user_id)
    )
    conn.commit()

    await callback.message.edit_text(
        f"✅ <b>Ежедневный чек-ин выполнен!</b>\n\n"
        f"🎁 Вы получили ⭐{reward} звёзд\n"
        f"📆 Возвращайтесь завтра за новой наградой!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")]
        ])
    )
@dp.callback_query(F.data == "leaderboard")
async def leaderboard(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Топ 10
    cursor.execute("""
        SELECT user_id, username, total_earned
        FROM users
        ORDER BY total_earned DESC
        LIMIT 10
    """)
    top_users = cursor.fetchall()

    text = "🏆 <b>Топ 10 игроков за месяц</b>\n\n"

    medals = ["🥇", "🥈", "🥉"]
    rewards = ["15$", "10$", "5$"]

    for i, (uid, username, total) in enumerate(top_users, start=1):

        medal = medals[i-1] if i <= 3 else f"{i}."

        masked = mask_username(username)
        if not masked:
            masked = mask_username(str(uid))

        reward_text = f" — 🎁 {rewards[i-1]}" if i <= 3 else ""

        text += f"{medal} {masked} — ⭐{total}{reward_text}\n"

    # Определяем место пользователя
    cursor.execute("""
        SELECT COUNT(*) + 1
        FROM users
        WHERE total_earned > (
            SELECT total_earned FROM users WHERE user_id = ?
        )
    """, (user_id,))
    place = cursor.fetchone()[0]

    cursor.execute("""
        SELECT total_earned FROM users WHERE user_id = ?
    """, (user_id,))
    user_total = cursor.fetchone()[0]

    text += (
        f"\n━━━━━━━━━━━━━━━\n"
        f"👤 Ваше место: <b>{place}</b>\n"
        f"⭐ Ваш результат: <b>{user_total}</b>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")]
        ])
    )

def mask_username(username: str) -> str:
    if not username:
        return None

    if len(username) <= 2:
        return username[0] + "*"

    return username[0] + "*" * (len(username) - 2) + username[-1]

@dp.callback_query(F.data == "my_balance")
async def handle_my_balance(callback: CallbackQuery):
    await safe_answer(callback)

    user_id = callback.from_user.id
    stars = get_user_stars(user_id)

    cursor.execute(
        "SELECT free_exchange_used FROM users WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    free_used = result[0] if result else 1

    free_text = (
        "❌ Бесплатный обмен уже использован"
        if free_used
        else "✅ Бесплатный обмен доступен"
    )

    await callback.message.edit_text(
        f"⭐ <b>Ваш баланс</b>\n\n"
        f"🌟 Звёзды: <b>{stars}</b>\n"
        f"{free_text}\n\n"
        f"💡 Получайте звёзды за:\n"
        f"• ежедневный чек-ин\n"
        f"• приглашение друзей\n"
        f"• активность в канале",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💱 Обменять звёзды", callback_data="exchange_menu")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")]
        ])
    )





def generate_voucher_code(length=10):
       chars = string.ascii_uppercase + string.digits
       return "STAR-" + "".join(random.choice(chars) for _ in range(length))



def add_or_update_user(user_id, user_name, user_surname, username, referrer_id):
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(
            "INSERT INTO users (user_id, user_name, user_surname, username, referrer_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, user_name, user_surname, username, referrer_id)
        )

        # 🎁 фиксированный бонус рефереру
        if referrer_id:
            cursor.execute(
                "UPDATE users SET stars = stars + 15 WHERE user_id = ?",
                (referrer_id,)
            )

    else:
        cursor.execute(
            "UPDATE users SET user_name = ?, user_surname = ?, username = ? WHERE user_id = ?",
            (user_name, user_surname, username, user_id)
        )

    conn.commit()

def has_accepted_rules(user_id: int) -> bool:
    cursor.execute("SELECT rules_accepted FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] == 1 if result else False

def accept_rules(user_id: int):
    cursor.execute("UPDATE users SET rules_accepted = 1 WHERE user_id = ?", (user_id,))
    conn.commit()

def get_user_stars(user_id: int) -> int:
    cursor.execute("SELECT stars FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

def add_stars(user_id: int, amount: int, tx_type="bonus", description="Начисление"):
    cursor.execute("UPDATE users SET stars = stars + ? WHERE user_id = ?", (amount, user_id))

    cursor.execute("""
        INSERT INTO star_transactions (user_id, amount, type, description, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, amount, tx_type, description, int(time.time())))

    conn.commit()


def select_gift(user_id: int, gift_code: str):
    cursor.execute("UPDATE users SET selected_gift = ? WHERE user_id = ?", (gift_code, user_id))
    conn.commit()

def get_selected_gift(user_id: int):
    cursor.execute("SELECT selected_gift FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def subtract_stars(user_id: int, amount: int, tx_type="exchange", description="Списание"):
    stars = get_user_stars(user_id)
    if stars >= amount:
        cursor.execute("UPDATE users SET stars = stars - ? WHERE user_id = ?", (amount, user_id))

        cursor.execute("""
            INSERT INTO star_transactions (user_id, amount, type, description, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, -amount, tx_type, description, int(time.time())))

        conn.commit()
        return True
    return False


# --- Keyboards ---
def build_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    for channel in OPEN_CHANNELS:
        builder.row(InlineKeyboardButton(text=OPEN_CHANNELS[channel], url=f"https://t.me/{channel.lstrip('@')}"))
    builder.row(InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subs"))
    return builder.as_markup()

def build_gift_options_keyboard():
    builder = InlineKeyboardBuilder()
    for key, cost in GIFT_STAR_COST.items():
        builder.row(InlineKeyboardButton(text=f"🎁 Подарок за ⭐{cost}", callback_data=f"gift_{key}"))
    return builder.as_markup()



def build_exchange_regular_keyboard():
    builder = InlineKeyboardBuilder()
    for key, cost in GIFT_STAR_COST.items():
        emoji = GIFT_EMOJIS.get(key, "🎁")
        builder.row(InlineKeyboardButton(text=f"{emoji} Обменять ⭐{cost}", callback_data=f"exchange_{key}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu"))
    return builder.as_markup()


def build_exchange_nft_keyboard():
    builder = InlineKeyboardBuilder()
    for key, (name, cost) in NFT_GIFTS.items():
        emoji = GIFT_EMOJIS.get(key, "🖼")
        if cost > 0:
            builder.row(InlineKeyboardButton(text=f"{emoji} {name} за ⭐{cost}", callback_data=f"exchange_nft_{key}"))
        else:
            builder.row(InlineKeyboardButton(text=f"{emoji} {name}", callback_data=f"exchange_nft_new"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu"))
    return builder.as_markup()

def build_exchange_stickers_keyboard():
    builder = InlineKeyboardBuilder()
    # Пока пустой, добавь сюда свои стикеры и цены, пример:
    # builder.row(InlineKeyboardButton(text="🔥 Стикер 1 за ⭐100", callback_data="exchange_sticker_1"))
    # builder.row(InlineKeyboardButton(text="❄ Стикер 2 за ⭐150", callback_data="exchange_sticker_2"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu"))
    return builder.as_markup()

async def check_open_channels(user_id):
    not_subscribed = []
    for channel in OPEN_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ("member", "administrator", "creator"):
                not_subscribed.append(channel)
        except Exception:
            not_subscribed.append(channel)
    return not_subscribed

# --- Handlers ---

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user = message.from_user
    user_id = user.id

    args = message.text.split()
    referrer_id = None
    if len(args) > 1:
        try:
            potential_referrer = int(args[1])
            if potential_referrer != user_id:
                referrer_id = potential_referrer
        except ValueError:
            pass

    add_or_update_user(user_id, user.first_name or "", user.last_name or "", user.username or "", referrer_id)

    selected_gift = get_selected_gift(user_id)
    if selected_gift:
        await message.answer(
            "🎁 <b>Вы уже выбрали свой подарок!</b>\n\n"
            "Ожидайте получение подарка после проведения проверки.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📈 Как повысить шансы получить подарок быстрее", callback_data="tips")],
                [InlineKeyboardButton(text="🎉 Мои бонусы за друзей", callback_data="ref_bonuses")],
                [InlineKeyboardButton(text="💱 Обменять звёзды на подарок", callback_data="exchange_menu")]
            ])
        )
        return

    await message.answer(
        "🎁 <b>Поздравляю, ты выиграл подарок!</b>\n\n"
        "Подпишись на канал @prosadin, чтобы выбрать какой именно ты хочешь 👇",
        reply_markup=build_subscription_keyboard()
    )
@dp.callback_query(F.data == "locked")
async def handle_locked_callback(callback: CallbackQuery):
    await callback.answer("❗ Для доступа к этой функции необходимо принять правила.", show_alert=True)
    await callback.message.answer(
        "📜 <b>Правила использования бота:</b>\n"
        "1. За приведение ботов по рефке - не выдаем подарок.\n"
        "2. Бот - юзер,который никак не проявляет активность.\n"
        "3. Активность - чтение постов,реакции,коменты.\n"
        "4. Обойти проверку невозможно.\n",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять правила", callback_data="accept_rules")]
        ])
    )
@dp.callback_query(F.data == "accept_rules")
async def accept_rules_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    accept_rules(user_id)  # обновляем в базе
    await callback.answer("Спасибо за принятие правил!", show_alert=True)
    # Обновляем меню после принятия правил
    await callback.message.edit_reply_markup(reply_markup=build_exchange_main_keyboard(user_id))




@dp.message(Command("createvoucher"))
async def create_voucher(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if (
            len(args) != 4
            or not args[1].isdigit()
            or not args[2].isdigit()
            or not args[3].isdigit()
    ):
        await message.answer(
            "❗ Использование:\n"
            "<code>/createvoucher звёзды всего_активаций на_человека</code>\n\n"
            "Пример:\n<code>/createvoucher 100 10 1</code>"
        )
        return

    stars = int(args[1])
    max_uses = int(args[2])
    per_user_limit = int(args[3])

    if stars <= 0 or max_uses <= 0 or per_user_limit <= 0:
        await message.answer("❗ Все значения должны быть больше 0.")
        return

    code = generate_voucher_code()
    now = int(time.time())

    cursor.execute(
        """
        INSERT INTO vouchers (code, stars, max_uses, per_user_limit, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (code, stars, max_uses, per_user_limit, now)
    )
    conn.commit()

    await message.answer(
        f"🎟 <b>Ваучер создан</b>\n\n"
        f"🔑 Код:\n<code>{code}</code>\n"
        f"⭐ Звёзды: <b>{stars}</b>\n"
        f"👥 Всего активаций: <b>{max_uses}</b>\n"
        f"👤 На человека: <b>{per_user_limit}</b>"
    )


@dp.message(Command("voucher"))
async def use_voucher(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()

    if len(args) != 2:
        await message.answer("❗ Использование:\n<code>/voucher CODE</code>")
        return

    code = args[1].upper()

    cursor.execute(
        """
        SELECT stars, max_uses, used_count, per_user_limit
        FROM vouchers WHERE code = ?
        """,
        (code,)
    )
    voucher = cursor.fetchone()

    if not voucher:
        await message.answer("❌ Ваучер не найден.")
        return

    stars, max_uses, used_count, per_user_limit = voucher

    if used_count >= max_uses:
        await message.answer("❌ Этот ваучер больше недоступен.")
        return

    # сколько раз этот пользователь уже активировал
    cursor.execute(
        "SELECT COUNT(*) FROM voucher_uses WHERE code = ? AND user_id = ?",
        (code, user_id)
    )
    user_uses = cursor.fetchone()[0]

    if user_uses >= per_user_limit:
        await message.answer("❌ Вы уже использовали этот ваучер максимальное число раз.")
        return

    # начисляем звёзды
    add_stars(user_id, stars)

    cursor.execute(
        "UPDATE vouchers SET used_count = used_count + 1 WHERE code = ?",
        (code,)
    )

    cursor.execute(
        "INSERT INTO voucher_uses (code, user_id, used_at) VALUES (?, ?, ?)",
        (code, user_id, int(time.time()))
    )

    conn.commit()

    await message.answer(
        f"🎉 <b>Ваучер активирован!</b>\n\n"
        f"⭐ Получено: <b>{stars}</b>\n"
        f"👤 Осталось для вас: <b>{per_user_limit - user_uses - 1}</b>\n"
        f"👥 Осталось всего: <b>{max_uses - used_count - 1}</b>"
    )

@dp.callback_query(F.data == "check_subs")
async def check_subscriptions(callback: CallbackQuery):
    # ✅ СРАЗУ отвечаем Telegram
    try:
        await safe_answer(callback)

    except:
        pass

    user_id = callback.from_user.id
    not_subscribed = await check_open_channels(user_id)

    if not not_subscribed:
        await callback.message.edit_text(
            "✅ <b>Вы подписались на все необходимые каналы!</b>\n\n"
            "<b>Выбери свой подарок из списка ниже:</b>\n"
            "❗ Первый обмен — бесплатный\n"
            "❗ Остальное — за рефов и актив\n"
            "❗ Чем дороже подарок, тем дольше проверка и больше нужно АКТИВА",
            reply_markup=build_exchange_main_keyboard(user_id)
        )
    else:
        # ❌ НЕ callback.answer здесь
        await callback.message.answer(
            "❗ Вы ещё не подписались на канал @prosadin"
        )


@dp.callback_query(F.data.startswith("gift_"))
async def handle_gift_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    gift_code = callback.data.replace("gift_", "")
    select_gift(user_id, gift_code)

    cursor.execute("SELECT referrer_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    referrer_id = result[0] if result else None
    if referrer_id:
        base_cost = GIFT_STAR_COST.get(gift_code, 0)
        bonus = int(base_cost * 0.3)
        add_stars(referrer_id, bonus)
        try:
            await bot.send_message(
                referrer_id,
                f"🎉 Ваш приглашённый друг выбрал подарок за ⭐{base_cost}. "
                f"Вы получили ⭐{bonus} бонусных звёзд!"
            )
        except Exception:
            pass

    await callback.message.edit_text(
        "🎉 <b>Отличный выбор!</b>\n\n"
        "Оставайтесь подписанным на канал @prosadin как можно большее количество дней, "
        "а также читайте посты, чтобы подтвердить, что вы не бот.\n\n"
        "📦 Как только вы пройдёте проверку, мы отправим вам подарок!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="confirm_back")]
        ])
    )

@dp.callback_query(F.data == "voucher_info")
async def voucher_info(callback: CallbackQuery):
    await safe_answer(callback)

    await callback.message.edit_text(
        "🎟 <b>Активация ваучера</b>\n\n"
        "Введите команду:\n"
        "<code>/voucher ВАШ-КОД</code>\n\n"
        "⚠ Ваучер одноразовый",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")]
        ])
    )



@dp.callback_query(F.data == "confirm_back")
async def handle_back_to_confirm(callback: CallbackQuery):
    await callback.message.edit_text(
        "✅ <b>Подарок успешно выбран!</b>\n\n"
        "Ожидайте получение подарка после проведения проверки.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👌 Окей", callback_data="ok")],
            [InlineKeyboardButton(text="📈 Как повысить шансы?", callback_data="tips")],
            [InlineKeyboardButton(text="💱 Обменять звёзды на подарок", callback_data="exchange_menu")]
        ])
    )

@dp.callback_query(F.data == "ok")
async def handle_ok(callback: CallbackQuery):
    await callback.message.edit_text(
        "👌 Спасибо! Мы свяжемся с вами, как только проверка будет завершена.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_after_ok")]
        ])
    )

@dp.callback_query(F.data == "back_after_ok")
async def handle_back_after_ok(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔙 Вы вернулись в меню. Выберите действие:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📈 Как повысить шансы получить подарок быстрее", callback_data="tips")],
            [InlineKeyboardButton(text="🎉 Мои бонусы за друзей", callback_data="ref_bonuses")],
            [InlineKeyboardButton(text="💱 Обменять звёзды на подарок", callback_data="exchange_menu")]
        ])
    )

@dp.callback_query(F.data == "tips")
async def handle_tips(callback: CallbackQuery):
    await callback.message.edit_text(
        "📈 <b>Как повысить шансы получить подарок быстрее?</b>\n\n"
        "• Оставайтесь подписанным на канал\n"
        "• Комментируйте и проявляйте активность\n"
        "• Приглашайте друзей — за каждого вы получите ⭐бонусы\n\n"
        "🎯 <b>Вы получаете 30% от стоимости подарка друга!</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📨 Пригласить друзей", callback_data="invite_friends")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_after_ok")]
        ])
    )

@dp.callback_query(F.data == "invite_friends")
async def handle_invite_friends(callback: CallbackQuery):
    user_id = callback.from_user.id
    link = f"https://t.me/test_pros_bot?start={user_id}"
    await callback.message.edit_text(
        f"📨 <b>Приглашай друзей и зарабатывай звёзды!</b>\n\n"
        f"Вот твоя реферальная ссылка:\n<code>{link}</code>\n\n"
        "🎁 За каждого друга — звёзды и бонусы!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="tips")]
        ])
    )

@dp.callback_query(F.data == "ref_bonuses")
async def handle_ref_bonuses(callback: CallbackQuery):
    user_id = callback.from_user.id
    stars = get_user_stars(user_id)

    await callback.message.edit_text(
        f"🌟 <b>Ваш баланс:</b> ⭐{stars} звёзд\n\n"
        "Приглашайте друзей и получайте 30% от стоимости их подарков!\n"
        "Звёзды можно обменивать на подарки.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_after_ok")]
        ])
    )

@dp.callback_query(F.data == "exchange_menu")
async def exchange_menu(callback: CallbackQuery):
    user_id = callback.from_user.id  # <--- Добавьте эту строку, чтобы получить user_id
    await callback.message.edit_text(
        "💱 <b>Обмен бонусных звёзд на подарки:</b>\n\n"
        "Выберите категорию подарков:",
        reply_markup=build_exchange_main_keyboard(user_id)  # Теперь user_id определён
    )

@dp.callback_query(F.data == "exchange_regular")
async def exchange_regular(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎁 <b>Основные подарки:</b>\n\n"
        "Выберите подарок для обмена:",
        reply_markup=build_exchange_regular_keyboard()
    )

@dp.callback_query(F.data == "exchange_nft")
async def exchange_nft(callback: CallbackQuery):
    await callback.message.edit_text(
        "🖼 <b>NFT подарки:</b>\n\n"
        "Выберите NFT подарок для обмена:",
        reply_markup=build_exchange_nft_keyboard()
    )


@dp.callback_query(F.data == "exchange_stickers")
async def exchange_stickers(callback: CallbackQuery):
    await callback.message.edit_text(
        "🖌 <b>Стикеры:</b>\n\n"
        "Выберите стикер для обмена:",
        reply_markup=build_exchange_stickers_keyboard()
    )
@dp.callback_query(F.data.startswith("exchange_cs_"))
async def handle_exchange_cs(callback: CallbackQuery):
    user_id = callback.from_user.id
    skin_key = callback.data.replace("exchange_cs_", "")

    skin = CS_SKINS.get(skin_key)
    if not skin:
        await callback.answer("❗ Скин недоступен.", show_alert=True)
        return

    gift_name, cost = skin
    stars = get_user_stars(user_id)

    if stars < cost:
        await callback.answer(
            f"❗ Недостаточно звёзд.\nНужно: {cost}, у вас: {stars}",
            show_alert=True
        )
        return

    # списываем
    subtract_stars(user_id, cost)

    # сохраняем подарок
    cursor.execute(
        "INSERT INTO user_gifts (user_id, gift_code, created_at) VALUES (?, ?, ?)",
        (user_id, skin_key, int(time.time()))
    )
    conn.commit()

    await callback.message.edit_text(
        f"🎉 <b>Вы успешно обменяли ⭐{cost}</b>\n\n"
        f"🎮 Скин: <b>{gift_name}</b>\n\n"
        "Ожидайте проверки и выдачи.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 В меню обмена", callback_data="exchange_menu")]
        ])
    )

@dp.callback_query(F.data == "exchange_cs")
async def exchange_cs_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎮 <b>Скины CS2</b>\n\nВыберите скин:",
        reply_markup=build_exchange_cs_keyboard()
    )

def build_exchange_stickers_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🐶 Стикер догс 9999 за ⭐400", callback_data="exchange_sticker_dogs9999"))
    builder.row(InlineKeyboardButton(text="🐾 Лост Догс за ⭐400", callback_data="exchange_sticker_lostdogs"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu"))
    return builder.as_markup()

@dp.callback_query(F.data == "exchange_nft_new")
async def handle_new_nft_gifts(callback: CallbackQuery):
    await bot.send_message(
        callback.from_user.id,
        " <b>Приглашайте друзей и проявляйте как можно большую активность, чтобы попасть в пул раздачи новых NFT!</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_nft")]
        ])
    )

@dp.callback_query(F.data.startswith("exchange_"))
async def handle_exchange_gift(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    gift_key = None
    gift_name = None
    cost = None
    is_standard_gift = False
    # 🎮 CS2 СКИНЫ — ПЕРВЫМИ
    if data.startswith("exchange_cs_"):
        skin_key = data.replace("exchange_cs_", "")
        skin = CS_SKINS.get(skin_key)

        if not skin:
            await callback.answer("❗ Скин недоступен.", show_alert=True)
            return

        gift_name, cost = skin
        gift_key = skin_key
    # NFT подарки
    if data.startswith("exchange_nft_"):
        gift_key = data.replace("exchange_nft_", "")
        gift = NFT_GIFTS.get(gift_key)
        if not gift or gift[1] == 0:
            await callback.answer("❗ Подарок недоступен. Ждём следующий праздник!", show_alert=True)
            return
        gift_name = gift[0]
        cost = gift[1]

    # Стикеры
    elif data.startswith("exchange_sticker_"):
        gift_key = data.replace("exchange_sticker_", "")
        if gift_key == "dogs9999":
            gift_name = "Стикер догс 9999"
            cost = 400
        elif gift_key == "lostdogs":
            gift_name = "Лост Догс"
            cost = 400
        else:
            await callback.answer("❗ Неизвестный стикер.", show_alert=True)
            return

    # Основные подарки
    else:
        gift_key = data.replace("exchange_", "")
        cost = GIFT_STAR_COST.get(gift_key)
        if cost is None:
            await callback.answer("❗ Неверный подарок.", show_alert=True)
            return
        gift_name = f"Подарок за ⭐{cost}"
        is_standard_gift = True

    # Проверка использован ли бесплатный обмен
    cursor.execute("SELECT free_exchange_used FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    free_used = result[0] if result else 1  # если нет записи, считаем как использованный

    # Условия бесплатного обмена:
    eligible_for_free = (
            is_standard_gift and
            cost <= 100 and
            free_used == 0
    )

    if eligible_for_free:
        # Отметим, что бесплатный обмен уже использован
        cursor.execute("UPDATE users SET free_exchange_used = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        select_gift(user_id, gift_key)
        cursor.execute(
            "INSERT INTO user_gifts (user_id, gift_code, created_at) VALUES (?, ?, ?)",
            (user_id, gift_key, int(time.time()))
        )
        conn.commit()
        await callback.message.edit_text(
            f"🎉 Ура! Ваш первый подарок за ⭐{cost} был получен <b>бесплатно</b>!\n\n"
            "Ожидайте подтверждения и получения подарка.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 В меню обмена", callback_data="exchange_menu")]
            ])
        )
        return

    # Если бесплатный обмен уже использован, проверяем баланс
    stars = get_user_stars(user_id)
    if stars < cost:
        await callback.answer(f"❗ У вас недостаточно звёзд. Нужно: {cost}, у вас: {stars}.", show_alert=True)
        return

    if subtract_stars(user_id, cost):
        select_gift(user_id, gift_key)
        cursor.execute(
            "INSERT INTO user_gifts (user_id, gift_code, created_at) VALUES (?, ?, ?)",
            (user_id, gift_key, int(time.time()))
        )
        conn.commit()
        await callback.message.edit_text(
            f"🎉 Поздравляем! Вы обменяли ⭐{cost} на: {gift_name}\n\n"
            "Ожидайте прохождения проверки и получения приза.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 В меню обмена", callback_data="exchange_menu")]
            ])
        )
    else:
        await callback.answer("❗ Не удалось списать звёзды.", show_alert=True)
@dp.message(Command("checkbonuce"))
async def handle_checkbonuce(message: types.Message):
    user_id = message.from_user.id
    stars = get_user_stars(user_id)
    await message.answer(
        f"🌟 <b>Ваш бонусный баланс:</b> ⭐{stars} звёзд",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_after_ok")]
        ])
    )


@dp.callback_query(F.data == "my_withdraw")
async def my_withdraw(callback: CallbackQuery):
    await safe_answer(callback)

    user_id = callback.from_user.id

    stars = get_user_stars(user_id)
    selected_gift = get_selected_gift(user_id)

    gift_text = (
        f"🎁 Текущий подарок: <b>{selected_gift}</b>"
        if selected_gift else
        "🎁 Подарок не выбран"
    )

    await callback.message.edit_text(
        f"📦 <b>Мои подарки и вывод</b>\n\n"
        f"⭐ Баланс: <b>{stars}</b>\n"
        f"{gift_text}\n\n"
        f"📤 Вы можете запросить вывод:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Запросить вывод звёзд", callback_data="withdraw_stars")],
            [InlineKeyboardButton(text="📜 История подарков", callback_data="history_gifts")],
            [InlineKeyboardButton(text="🎁 Запросить выдачу подарка", callback_data="withdraw_gift")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")]
        ])

    )

@dp.callback_query(F.data == "history_gifts")
async def history_gifts(callback: CallbackQuery):
    await safe_answer(callback)
    user_id = callback.from_user.id

    cursor.execute(
        """
        SELECT gift_code, status, created_at
        FROM user_gifts
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()

    if not rows:
        await callback.message.edit_text(
            "📜 <b>История подарков</b>\n\n"
            "У вас пока нет подарков.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="my_withdraw")]
            ])
        )
        return

    def status_text(status: str) -> str:
        return {
            "pending": "⏳ Ожидает",
            "requested": "📤 Запрошен",
            "delivered": "✅ Получен"
        }.get(status, status)

    text = "📜 <b>История подарков</b>\n\n"

    for gift_code, status, created_at in rows:
        date = time.strftime("%d.%m.%Y %H:%M", time.localtime(created_at))
        text += (
            f"🎁 <b>{gift_name(gift_code)}</b>\n"
            f"📌 Статус: {status_text(status)}\n"
            f"🕒 {date}\n\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="my_withdraw")]
        ])
    )


@dp.callback_query(F.data == "withdraw_stars")
async def withdraw_stars(callback: CallbackQuery):
    await safe_answer(callback)

    user_id = callback.from_user.id
    stars = get_user_stars(user_id)

    if stars < MIN_WITHDRAW_STARS:
        await callback.message.answer(
            f"❗ Минимальный вывод: ⭐{MIN_WITHDRAW_STARS}\n"
            f"У вас: ⭐{stars}"
        )
        return

    cursor.execute(
        "INSERT INTO withdrawals (user_id, type, amount, created_at) VALUES (?, 'stars', ?, ?)",
        (user_id, stars, int(time.time()))
    )

    cursor.execute(
        "UPDATE users SET stars = 0 WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()

    await callback.message.answer(
        "✅ <b>Заявка на вывод звёзд создана!</b>\n"
        "Администратор свяжется с вами."
    )

@dp.message(Command("withdrawals"))
async def admin_withdrawals(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("""
    SELECT id, user_id, type, amount, gift_code, status, created_at
    FROM withdrawals
    WHERE status = 'pending'
    ORDER BY created_at ASC
""")
    rows = cursor.fetchall()

    if not rows:
        await message.answer("📭 Нет заявок на вывод.")
        return

    for w_id, user_id, w_type, amount, gift_code, status, created_at in rows:
        date = time.strftime("%d.%m.%Y %H:%M", time.localtime(created_at))

        text = (
            f"📤 <b>Заявка #{w_id}</b>\n"
            f"👤 User ID: <code>{user_id}</code>\n"
            f"🕒 {date}\n"
        )

        if w_type == "stars":
            text += f"⭐ Звёзды: <b>{amount}</b>\n"
        else:
            text += f"🎁 Подарок: <b>{gift_name(gift_code)}</b>\n"

        text += f"📌 Статус: <b>{status}</b>"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f"admin_ok_{w_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{w_id}")

            ]
        ])

        await message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data.startswith("admin_ok_"))
async def admin_approve(callback: CallbackQuery):
    await safe_answer(callback)

    if callback.from_user.id != ADMIN_ID:
        return

    w_id = int(callback.data.replace("admin_ok_", ""))

    # 1️⃣ данные заявки
    cursor.execute("""
        SELECT user_id, type, amount, gift_code
        FROM withdrawals
        WHERE id = ? AND status = 'pending'
    """, (w_id,))
    row = cursor.fetchone()

    if not row:
        await callback.message.edit_text("❌ Заявка не найдена или уже обработана.")
        return

    user_id, w_type, amount, gift_code = row

    # 2️⃣ referrer
    cursor.execute(
        "SELECT referrer_id FROM users WHERE user_id = ?",
        (user_id,)
    )
    ref_row = cursor.fetchone()
    referrer_id = ref_row[0] if ref_row else None

    # 3️⃣ обновляем статус заявки
    cursor.execute(
        "UPDATE withdrawals SET status = 'approved' WHERE id = ?",
        (w_id,)
    )
    conn.commit()

    # 4️⃣ реферальный бонус 30%
    if referrer_id:
        if w_type == "stars":
            bonus = int(amount * 0.3)
        else:
            gift_price = GIFT_PRICES.get(gift_code, 0)
            bonus = int(gift_price * 0.3)

        if bonus > 0:
            cursor.execute(
                "UPDATE users SET stars = stars + ? WHERE user_id = ?",
                (bonus, referrer_id)
            )
            conn.commit()

            # уведомление рефереру
            try:
                await bot.send_message(
                    referrer_id,
                    f"🎉 <b>Реферальный бонус!</b>\n\n"
                    f"👤 Ваш реферал получил вывод\n"
                    f"💰 Бонус: ⭐{bonus}"
                )
            except:
                pass

    # 5️⃣ уведомление пользователю
    try:
        if w_type == "gift":
            await bot.send_message(
                user_id,
                f"🎁 <b>Подарок выдан!</b>\n\n"
                f"{gift_name(gift_code)}"
            )
        else:
            await bot.send_message(
                user_id,
                f"⭐ <b>Вывод одобрен!</b>\n"
                f"Сумма: {amount}"
            )
    except:
        pass

    # 6️⃣ лог
    await bot.send_message(
        LOG_CHANNEL_ID,
        f"✅ <b>ОДОБРЕНО</b>\n"
        f"📤 Заявка #{w_id}\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"🤝 Реферер: <code>{referrer_id or '—'}</code>"
    )

    await callback.message.edit_text("✅ Заявка одобрена.")


@dp.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return

    withdrawal_id = int(callback.data.replace("admin_reject_", ""))

    await state.set_state(RejectFSM.typing_reason)
    await state.update_data(
        withdrawal_id=withdrawal_id,
        reason_text=""
    )

    await callback.message.answer(
        "❌ <b>Введите причину отказа</b>\n\n"
        "Вы можете отправить <b>несколько сообщений</b>.\n"
        "Когда закончите — нажмите кнопку <b>«Готово»</b>.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Готово", callback_data="reject_done")]
        ])
    )
    await callback.answer()


@dp.message(RejectFSM.typing_reason)
async def collect_reject_reason(message: Message, state: FSMContext):
    data = await state.get_data()
    current = data.get("reason_text", "")

    new_text = current + "\n" + message.text if current else message.text

    await state.update_data(reason_text=new_text)

    await message.answer("✍️ Принято. Можете дописать ещё или нажать «Готово».")



@dp.callback_query(F.data == "reject_done")
async def finish_reject(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return

    data = await state.get_data()
    withdrawal_id = data["withdrawal_id"]
    reason = data.get("reason_text", "").strip()

    if not reason:
        reason = "Заявка отклонена администратором."

    cursor.execute(
        "SELECT user_id FROM withdrawals WHERE id = ?",
        (withdrawal_id,)
    )
    row = cursor.fetchone()
    if not row:
        await callback.message.answer("❗ Заявка не найдена")
        await state.clear()
        return

    user_id = row[0]

    # обновляем статус
    cursor.execute(
        "UPDATE withdrawals SET status = 'rejected' WHERE id = ?",
        (withdrawal_id,)
    )
    conn.commit()

    # 🔔 уведомление пользователю
    try:
        await bot.send_message(
            user_id,
            f"❌ <b>Ваша заявка отклонена</b>\n\n"
            f"📄 Причина:\n<blockquote>{reason}</blockquote>"
        )
    except:
        pass

    # 📝 лог в канал
    await bot.send_message(
        LOG_CHANNEL_ID,
        f"❌ <b>ОТКАЗ</b>\n"
        f"📤 Заявка #{withdrawal_id}\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"📄 Причина:\n{reason}"
    )

    await callback.message.edit_text("❌ Заявка отклонена и пользователь уведомлён.")
    await state.clear()





@dp.message(RejectReason.waiting_for_reason)
async def admin_reject_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    withdrawal_id = data["withdrawal_id"]

    reason = message.text.strip()
    if reason == ".":
        reason = "Заявка отклонена администратором."

    # получаем user_id
    cursor.execute(
        "SELECT user_id FROM withdrawals WHERE id = ?",
        (withdrawal_id,)
    )
    row = cursor.fetchone()
    if not row:
        await message.answer("❗ Заявка не найдена")
        await state.clear()
        return

    user_id = row[0]

    # обновляем статус
    cursor.execute(
        "UPDATE withdrawals SET status = 'rejected' WHERE id = ?",
        (withdrawal_id,)
    )
    conn.commit()

    # уведомляем пользователя
    try:
        await bot.send_message(
            user_id,
            f"❌ <b>Ваша заявка отклонена</b>\n\n"
            f"📄 Причина:\n<blockquote>{reason}</blockquote>"
        )
    except Exception:
        pass

    # лог админу
    await bot.send_message(
        LOG_CHANNEL_ID,
        f"❌ <b>ОТКЛОНЕНИЕ</b>\n"
        f"📤 Заявка #{withdrawal_id}\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"📄 Причина: {reason}"
    )

    await message.answer("❌ Заявка отклонена")
    await state.clear()




@dp.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    withdrawal_id = int(callback.data.split("_")[-1])

    cursor.execute(
        "SELECT user_id FROM withdrawals WHERE id = ?",
        (withdrawal_id,)
    )
    row = cursor.fetchone()

    if not row:
        await callback.answer("❗ Заявка не найдена", show_alert=True)
        return

    user_id = row[0]

    cursor.execute(
        "UPDATE withdrawals SET status = 'rejected' WHERE id = ?",
        (withdrawal_id,)
    )
    conn.commit()

    # уведомление пользователю
    await bot.send_message(
        user_id,
        "❌ <b>Ваша заявка на вывод отклонена.</b>\n\n"
        "Если вы считаете это ошибкой — свяжитесь с поддержкой."
    )

    await callback.message.edit_text("❌ Заявка отклонена")




@dp.callback_query(F.data == "withdraw_gift")
async def withdraw_gift(callback: CallbackQuery):
    await safe_answer(callback)
    user_id = callback.from_user.id

    cursor.execute(
        """
        SELECT id, gift_code
        FROM user_gifts
        WHERE user_id = ? AND status = 'pending'
        """,
        (user_id,)
    )
    gifts = cursor.fetchall()

    if not gifts:
        await callback.message.answer("❗ У вас нет доступных подарков для вывода.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"🎁 {gift_code}",
                callback_data=f"withdraw_gift_{gift_id}"
            )
        ]
        for gift_id, gift_code in gifts
    ])


    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="my_withdraw")]
    )

    await callback.message.edit_text(
        "📦 <b>Ваши подарки</b>\n\n"
        "Выберите подарок для вывода:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data.startswith("withdraw_gift_"))
async def withdraw_specific_gift(callback: CallbackQuery):
    await safe_answer(callback)
    user_id = callback.from_user.id
    gift_id = int(callback.data.replace("withdraw_gift_", ""))

    cursor.execute(
        """
        SELECT gift_code FROM user_gifts
        WHERE id = ? AND user_id = ? AND status = 'pending'
        """,
        (gift_id, user_id)
    )
    row = cursor.fetchone()

    if not row:
        await callback.answer("❗ Подарок недоступен.", show_alert=True)
        return

    gift_code = row[0]

    cursor.execute(
        "UPDATE user_gifts SET status = 'requested' WHERE id = ?",
        (gift_id,)
    )

    cursor.execute(
        """
        INSERT INTO withdrawals (user_id, type, gift_code, gift_id, created_at)
        VALUES (?, 'gift', ?, ?, ?)
        """,
        (user_id, gift_code, gift_id, int(time.time()))
    )
    cursor.execute(
        "UPDATE user_gifts SET status = 'requested' WHERE id = ?",
        (gift_id,)
    )


    conn.commit()

    await callback.message.edit_text(
        f"🎁 <b>Заявка на вывод подарка отправлена!</b>\n\n"
        f"Подарок: <b>{gift_code}</b>\n"
        "Ожидайте подтверждения."
    )

@dp.callback_query(F.data.startswith("admin_ok_"))
async def admin_approve(callback: CallbackQuery):
    await safe_answer(callback)

    if callback.from_user.id != ADMIN_ID:
        return

    w_id = int(callback.data.replace("admin_ok_", ""))

    # данные заявки
    cursor.execute("""
        SELECT user_id, type, gift_id, gift_code, amount
        FROM withdrawals
        WHERE id = ? AND status = 'pending'
    """, (w_id,))
    row = cursor.fetchone()

    if not row:
        await callback.message.edit_text("❌ Заявка не найдена или уже обработана.")
        return

    user_id, w_type, gift_id, gift_code, amount = row

    # одобряем заявку
    cursor.execute(
        "UPDATE withdrawals SET status = 'approved' WHERE id = ?",
        (w_id,)
    )

    # если подарок — помечаем как выданный
    if w_type == "gift" and gift_id:
        cursor.execute(
            "UPDATE user_gifts SET status = 'delivered' WHERE id = ?",
            (gift_id,)
        )

    conn.commit()

    # ───── РЕФЕРАЛЬНЫЙ БОНУС 30% ─────
    cursor.execute(
        "SELECT referrer_id FROM users WHERE user_id = ?",
        (user_id,)
    )
    ref_row = cursor.fetchone()
    referrer_id = ref_row[0] if ref_row else None

    if referrer_id:
        if w_type == "stars":
            bonus = int(amount * 0.3)
        else:
            gift_price = GIFT_PRICES.get(gift_code, 0)
            bonus = int(gift_price * 0.3)

        if bonus > 0:
            cursor.execute(
                "UPDATE users SET stars = stars + ? WHERE user_id = ?",
                (bonus, referrer_id)
            )
            conn.commit()

            try:
                await bot.send_message(
                    referrer_id,
                    f"🎉 <b>Реферальный бонус!</b>\n\n"
                    f"👤 Ваш реферал получил вывод\n"
                    f"💰 Бонус: ⭐{bonus}"
                )
            except:
                pass

    # 📝 лог в админ-канал
    await bot.send_message(
        LOG_CHANNEL_ID,
        f"✅ <b>ОДОБРЕНО</b>\n"
        f"📤 Заявка #{w_id}\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"🎁 Тип: {w_type}\n"
        f"📦 Детали: {gift_name(gift_code) if gift_code else amount}"
    )

    # 🔔 уведомление пользователю
    try:
        if w_type == "gift":
            await bot.send_message(
                user_id,
                f"🎉 <b>Ваш подарок выдан!</b>\n\n"
                f"🎁 Подарок: <b>{gift_name(gift_code)}</b>\n"
                f"Спасибо за участие ❤️"
            )
        else:
            await bot.send_message(
                user_id,
                f"🎉 <b>Ваши звёзды успешно выведены!</b>\n"
                f"⭐ Сумма: <b>{amount}</b>\n"
                "Спасибо за участие ❤️"
            )
    except:
        pass

    await callback.message.edit_text("✅ Заявка одобрена и обработана.")

@dp.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery):
    await safe_answer(callback)

    if callback.from_user.id != ADMIN_ID:
        return

    w_id = int(callback.data.replace("admin_reject_", ""))

    cursor.execute(
        "UPDATE withdrawals SET status = 'rejected' WHERE id = ?",
        (w_id,)
    )
    conn.commit()


    await callback.message.edit_text("❌ Заявка отклонена.")





@dp.message(Command("deliver_gift"))
async def deliver_gift(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer(
            "❗ Использование:\n<code>/deliver_gift ID_ПОДАРКА</code>"
        )
        return

    gift_id = int(args[1])

    cursor.execute(
        "UPDATE user_gifts SET status = 'delivered' WHERE id = ?",
        (gift_id,)
    )

    if cursor.rowcount == 0:
        await message.answer("❌ Подарок не найден.")
        return

    conn.commit()
    await message.answer("✅ Подарок отмечен как выданный.")




@dp.message(Command("myref"))
async def handle_myref(message: types.Message):
    user_id = message.from_user.id
    link = f"https://t.me/test_pros_bot?start={user_id}"
    await message.answer(
        f"📨 <b>Ваша реферальная ссылка:</b>\n<code>{link}</code>\n\n"
        "Приглашайте друзей и получайте ⭐бонусы за их действия!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_after_ok")]
        ])
    )

# 1. Создаём состояния
class Broadcast(StatesGroup):
    waiting_for_text = State()

# 2. Команда для запуска рассылки
@dp.message(Command("broadcast"))
async def start_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет доступа.")
        return
    await message.answer("📢 Введите текст рассылки:")
    await state.set_state(Broadcast.waiting_for_text)

# 3. Обработка текста и рассылка
@dp.message(Broadcast.waiting_for_text)
async def send_broadcast(message: types.Message, state: FSMContext):
    text_to_send = message.text
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    success = 0
    fail = 0
    for (user_id,) in users:
        try:
            await bot.send_message(user_id, text_to_send)
            success += 1
        except Exception as e:
            print(f"Не доставлено {user_id}: {e}")  # <--- добавь это
            fail += 1

    await message.answer(f"✅ Рассылка завершена.\nУспешно: {success}, Не доставлено: {fail}")
    await state.clear()  # <-- завершаем FSM

@dp.message()
async def auto_nickname_bonus_check(message: Message):
    print("USERNAME:", message.from_user.username)
    print("FIRST_NAME:", message.from_user.first_name)
    print("LAST_NAME:", message.from_user.last_name)
    print("-----")

    user_id = message.from_user.id
    username = message.from_user.username
    now = int(time.time())

    cursor.execute("""
        SELECT nickname_bonus_last, nickname_bonus_blocked_until
        FROM users WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()

    if not row:
        return

    last_bonus, blocked_until = row

    # ===== РАЗБЛОКИРОВКА =====
    if blocked_until and now >= blocked_until:
        cursor.execute("""
            UPDATE users SET nickname_bonus_blocked_until = 0
            WHERE user_id = ?
        """, (user_id,))
        conn.commit()

        await message.answer("✅ Блокировка бонуса снята! Можешь снова получать +5 ⭐")

        blocked_until = 0

    # ===== ЕСЛИ В БАНЕ =====
    if blocked_until and now < blocked_until:
        return

    # ===== ПРОВЕРКА НИКА =====
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""

    full_name = f"{first_name} {last_name}".lower()

    has_tag = "@prosadin" in full_name

    if has_tag:
        # 24 часа
        if now - last_bonus >= 86400:
            add_stars(user_id, 5)

            cursor.execute("""
                UPDATE users SET nickname_bonus_last = ?
                WHERE user_id = ?
            """, (now, user_id))
            conn.commit()

            await message.answer("💎 +5 ⭐ за ник @prosadin!")
    else:
        # если раньше бонус был активен — блок
        if last_bonus != 0:
            block_until = now + 3 * 86400

            cursor.execute("""
                UPDATE users
                SET nickname_bonus_last = 0,
                    nickname_bonus_blocked_until = ?
                WHERE user_id = ?
            """, (block_until, user_id))
            conn.commit()

            await message.answer(
                "❌ Ты убрал @prosadin из ника.\n"
                "Бонус заблокирован на 3 дня."
            )
@dp.callback_query(F.data == "nickname_bonus")
async def nickname_bonus_status(callback: CallbackQuery):
    await safe_answer(callback)

    user_id = callback.from_user.id
    now = int(time.time())

    cursor.execute("""
        SELECT nickname_bonus_last, nickname_bonus_blocked_until
        FROM users WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()

    if not row:
        return

    last_bonus, blocked_until = row

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить снова", callback_data="nickname_bonus_refresh")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="exchange_menu")]
    ])

    # ===== ЕСЛИ ЗАБЛОКИРОВАН =====
    if blocked_until and now < blocked_until:
        remaining = blocked_until - now
        days_left = remaining // 86400 + 1
        total = 3
        progress = total - days_left
        progress_text = f"{progress}/{total} дней"

        text = (
            f"🚫 <b>Бонус заблокирован</b>\n\n"
            f"⏳ Осталось: <b>{days_left}</b> дн.\n"
            f"📊 Прогресс: <b>{progress_text}</b>"
        )

    # ===== ЕСЛИ НЕ В БАНЕ =====
    else:
        first_name = callback.from_user.first_name or ""
        last_name = callback.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".lower()

        if "@prosadin" in full_name:
            text = (
                "✅ <b>Ник активен</b>\n\n"
                "💎 Вы получаете +5 ⭐ каждые 24 часа\n"
                "Не удаляйте @prosadin из ника."
            )
        else:
            text = (
                "❌ <b>В нике нет @prosadin</b>\n\n"
                "Добавьте его, чтобы получать +5 ⭐ ежедневно."
            )

    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest:
        pass

@dp.callback_query(F.data == "nickname_bonus_refresh")
async def nickname_bonus_refresh(callback: CallbackQuery):
    await safe_answer(callback)

    user_id = callback.from_user.id
    username = callback.from_user.username
    now = int(time.time())

    cursor.execute("""
        SELECT nickname_bonus_last, nickname_bonus_blocked_until
        FROM users WHERE user_id = ?
    """, (user_id,))
    last_bonus, blocked_until = cursor.fetchone()

    # ===== РАЗБЛОКИРОВКА =====
    if blocked_until and now >= blocked_until:
        cursor.execute("""
            UPDATE users
            SET nickname_bonus_blocked_until = 0
            WHERE user_id = ?
        """, (user_id,))
        conn.commit()
        blocked_until = 0

    # ===== ЕСЛИ ВСЁ ЕЩЁ В БАНЕ =====
    if blocked_until and now < blocked_until:
        await callback.answer("⏳ Бонус ещё заблокирован.", show_alert=True)
        return

    # ===== ПРОВЕРКА НИКА =====
    first_name = callback.from_user.first_name or ""
    last_name = callback.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".lower()

    if "@prosadin" in full_name:

        if now - last_bonus >= 86400:
            add_stars(user_id, 5)

            cursor.execute("""
                UPDATE users SET nickname_bonus_last = ?
                WHERE user_id = ?
            """, (now, user_id))
            conn.commit()

            await callback.answer("💎 +5 ⭐ начислено!", show_alert=True)
        else:
            await callback.answer("⏳ 24 часа ещё не прошли.", show_alert=True)
    else:
        await callback.answer("❌ В нике нет @prosadin.", show_alert=True)

    # Обновляем экран
    await nickname_bonus_status(callback)



if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))