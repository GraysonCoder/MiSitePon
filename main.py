# Обновлённый Telegram-бот: кнопка "🛒 Купить", бесплатное скачивание читов
# Все читы доступны бесплатно, оплата временно отключена

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    FSInputFile
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime

BOT_TOKEN = "8189908186:AAF_nXDaGpU3dCmlNTVdAZtUIsP6V8AdxQY"
ADMIN_ID = 7019630461

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# FSM для скрина оплаты
class Purchase(StatesGroup):
    waiting_for_screenshot = State()

# Список читов: (название, описание, filename.zip)
CHEATS = {
    "cheat1": ("StandShaer old cheat", "Старый чит для StandShaer. Работает стабильно.", "cheat1.zip"),
    "cheat2": ("StandShaer New cheat", "Новая версия чита StandShaer.", "cheat2.zip"),
    "cheat3": ("Stand52 V1 cheat mobile", "Stand52 V1 для мобильных устройств.", "cheat3.zip"),
    "cheat4": ("Stand52 V2 cheat mobile", "Новая версия Stand52 V2 для Android.", "cheat4.zip"),
    "cheat5": ("Stand52 V1 cheat Pc", "Stand52 версия 1 для ПК.", "cheat5.zip"),
    "cheat6": ("Stand52 V2 cheat Pc", "Stand52 версия 2 для ПК.", "cheat6.zip"),
}

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мой ЛС", url="@sn0wbypass")],
        [InlineKeyboardButton(text="Канал", url="https://t.me/+mDO77mr4jxxhZjdi")],
        [InlineKeyboardButton(text="🛒 Купить", callback_data="buy_menu")],
        [InlineKeyboardButton(text="Предложить чит", callback_data="suggest")]
    ])

# Меню читов
def cheats_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        *[
            [InlineKeyboardButton(text=f"📄 {title}", callback_data=f"cheat_{key}")]
            for key, (title, _, _) in CHEATS.items()
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

# Кнопка скачивания
def free_download_keyboard(cheat_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬇️ Скачать бесплатно", callback_data=f"free_{cheat_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="buy_menu")]
    ])

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=main_menu())

@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_menu())

@dp.callback_query(F.data == "buy_menu")
async def buy_menu(callback: CallbackQuery):
    text = (
        "🛒 <b>Магазин</b>\n\n"
        "💬 <i>Оплата читов временно недоступна.</i>\n"
        "<b>Все читы доступны бесплатно.</b>\n\n"
        "Выбери нужный чит:"
    )
    await callback.message.edit_text(text, reply_markup=cheats_keyboard())

@dp.callback_query(F.data.startswith("cheat_"))
async def show_cheat(callback: CallbackQuery):
    cheat_id = callback.data.split("_")[1]
    title, desc, _ = CHEATS[cheat_id]
    await callback.message.edit_text(
        f"<b>{title}</b>\n\n{desc}",
        reply_markup=free_download_keyboard(cheat_id)
    )

@dp.callback_query(F.data.startswith("free_"))
async def send_free_file(callback: CallbackQuery):
    cheat_id = callback.data.split("_")[1]
    title, _, filename = CHEATS[cheat_id]
    try:
        file = FSInputFile(path=f"files/{filename}")
        await bot.send_document(callback.from_user.id, file, caption=f"<b>{title}</b>\n⬇️ Спасибо за скачивание!")
        await callback.answer("Файл отправлен ✅", show_alert=True)
    except Exception:
        await callback.answer("Файл не найден ❌", show_alert=True)

@dp.callback_query(F.data == "suggest")
async def suggest_handler(callback: CallbackQuery):
    await bot.send_message(callback.from_user.id,
                           "✉️ Отправь описание чита, который хочешь предложить. Я передам админам.")
    await callback.answer()

@dp.message(F.text & ~F.via_bot)
async def catch_suggestions(message: Message):
    if message.chat.type == "private":
        await bot.send_message(
            ADMIN_ID,
            f"📬 <b>Предложение чита</b> от @{message.from_user.username or message.from_user.id}:\n\n{message.text}"
        )
        await message.reply("✅ Спасибо! Мы рассмотрим твоё предложение.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

