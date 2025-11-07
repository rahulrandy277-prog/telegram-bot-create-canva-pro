import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# ---------------------------
# Env & logging
# ---------------------------
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("canva_pro_bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")  # <-- from env
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@kashsh00")

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN. Put it in .env or your hosting env.")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
dp = Dispatcher()
router = Router()  # <-- use Router for decorators

# ---------------------------
# Commands setup
# ---------------------------
async def set_bot_commands(b: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="plans", description="View Canva Pro pricing"),
        BotCommand(command="buy", description="Buy Canva Pro Premium"),
        BotCommand(command="whyus", description="Why choose us?"),
        BotCommand(command="reviews", description="See user reviews"),
        BotCommand(command="help", description="Get help or contact admin"),
    ]
    await b.set_my_commands(commands)

# ---------------------------
# Keyboards
# ---------------------------
def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="💰 View Plans", callback_data="plans"),
        InlineKeyboardButton(text="🛍️ Buy Now", callback_data="buy"),
    )
    kb.row(
        InlineKeyboardButton(text="🎓 Try Free Trial", callback_data="trial"),
        InlineKeyboardButton(text="⭐ Reviews", callback_data="reviews"),
    )
    kb.row(
        InlineKeyboardButton(text="🧠 Why Choose Us", callback_data="whyus"),
        InlineKeyboardButton(text="📞 Contact", callback_data="help"),
    )
    return kb.as_markup()

def back_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="back")]]
    )

# ---------------------------
# Handlers (Router decorators)
# ---------------------------
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🎨 **Welcome to Canva Pro Premium Access Bot!**\n\n"
        "💎 *Design without limits* — Get genuine **Canva Pro** instantly!\n\n"
        "✅ 100% Safe & Verified (No cracked or illegal accounts)\n"
        "⚡ Instant Delivery | 🎓 Lifetime & Team Access | 🔒 Secure & Trusted\n\n"
        f"👨‍💼 Admin Support: {ADMIN_USERNAME}\n\n"
        "👇 Choose an option below to begin your journey:",
        reply_markup=main_menu(),
    )

@router.message(Command("plans"))
async def plans_command(message: types.Message):
    await message.answer(
        "💰 **Canva Pro Premium Plans**\n\n"
        "🟢 1 Month Access — ₹50\n"
        "🟡 3 Months Access — ₹120\n"
        "🔵 6 Months Access — ₹200\n"
        "💎 Lifetime Access — ₹499\n\n"
        "🎓 Education Plans Available (For Students & Creators)\n\n"
        "⚡ *Instant activation after verification!*",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🛍️ Buy Now", callback_data="buy")],
                [InlineKeyboardButton(text="⬅️ Back", callback_data="back")],
            ]
        ),
    )

@router.message(Command("whyus"))
async def whyus_command(message: types.Message):
    await message.answer(
        "🧠 **Why Choose Us?**\n\n"
        "✅ We don’t sell cracked or fake accounts.\n"
        "🔐 All accounts are 100% safe & verified.\n"
        "⚡ Instant delivery with lifetime replacement guarantee.\n"
        "🎓 Special student access for education users.\n"
        "💬 24×7 active support — we care about your satisfaction!\n\n"
        "💎 *Join thousands of happy Canva users today!*",
        reply_markup=back_button(),
    )

@router.message(Command("buy"))
async def buy_command(message: types.Message):
    await message.answer(
        "🛍️ **Buy Canva Pro Now**\n\n"
        f"💬 Contact Admin: {ADMIN_USERNAME}\n\n"
        "💎 Pay only after verification ✅\n"
        "⚡ Instant access once confirmed\n"
        "🎨 Start designing like a pro within minutes!",
        reply_markup=back_button(),
    )

@router.message(Command("reviews"))
async def reviews_command(message: types.Message):
    await message.answer(
        "⭐ **Customer Reviews** ⭐\n\n"
        "👩‍🎨 ‘Got my account in 2 minutes. Legit and smooth!’\n"
        "👨‍💻 ‘Best service ever! I’ve been using Canva Pro daily.’\n"
        "🎓 ‘Loved the student plan. Highly recommended!’\n\n"
        "💬 Want to share your feedback?\n"
        f"Message {ADMIN_USERNAME} ❤️",
        reply_markup=back_button(),
    )

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "💬 **Need Help or Have Questions?**\n\n"
        f"📞 Contact Admin: {ADMIN_USERNAME}\n"
        "⚡ We reply instantly — your satisfaction is our top priority!\n"
        "🎯 Whether it’s setup, payment, or renewal — we’re here 24×7.",
        reply_markup=back_button(),
    )

@router.callback_query(F.data.in_({"plans", "buy", "whyus", "reviews", "trial", "help", "back"}))
async def handle_buttons(callback: types.CallbackQuery):
    data = callback.data
    if data == "plans":
        await callback.message.edit_text(
            "💰 **Our Canva Pro Plans**\n\n"
            "🟢 1 Month — ₹50\n"
            "🟡 3 Months — ₹120\n"
            "🔵 6 Months — ₹200\n"
            "💎 Lifetime — ₹499\n\n"
            "🎓 Education Plans Available!\n"
            "Click *Buy Now* to get started 👇",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🛍️ Buy Now", callback_data="buy")],
                    [InlineKeyboardButton(text="⬅️ Back", callback_data="back")],
                ]
            ),
        )
    elif data == "buy":
        await callback.message.edit_text(
            "🛍️ **Buy Canva Pro Premium**\n\n"
            f"👨‍💼 Contact Admin: {ADMIN_USERNAME}\n\n"
            "💎 Pay After Verification ✅\n"
            "⚡ Instant Delivery | 100% Secure",
            reply_markup=back_button(),
        )
    elif data == "whyus":
        await callback.message.edit_text(
            "🧠 **Why Choose Us?**\n\n"
            "✅ Genuine Canva Pro — No cracked or risky accounts.\n"
            "🔒 Safe & Verified with instant access.\n"
            "🎓 Student access available.\n"
            "💬 24×7 Customer Support.\n\n"
            "💎 *Trusted by 5000+ users across India!*",
            reply_markup=back_button(),
        )
    elif data == "reviews":
        await callback.message.edit_text(
            "⭐ **User Reviews** ⭐\n\n"
            "🧑‍🎨 ‘Got Canva Pro in 2 minutes! Excellent service.’\n"
            "👩‍💻 ‘Very supportive admin, helped instantly.’\n"
            "🎓 ‘Perfect for students & freelancers.’",
            reply_markup=back_button(),
        )
    elif data == "trial":
        await callback.message.edit_text(
            "🎓 **Free Trial Access**\n\n"
            "👋 Get a short Canva Pro trial absolutely FREE!\n"
            "💬 Contact Admin to claim your trial now:\n"
            f"{ADMIN_USERNAME}\n\n"
            "⚡ Limited spots available — don’t miss it!",
            reply_markup=back_button(),
        )
    elif data == "help":
        await callback.message.edit_text(
            f"💬 Need Help?\n\n📞 Contact {ADMIN_USERNAME}\nWe’re available 24×7 ❤️",
            reply_markup=back_button(),
        )
    elif data == "back":
        await callback.message.edit_text(
            "🎨 **Welcome Back! Choose an option below 👇",
            reply_markup=main_menu(),
        )

    await callback.answer()

# ---------------------------
# Lifecycle & run
# ---------------------------
@dp.startup()
async def on_startup():
    log.info("Setting bot commands…")
    await set_bot_commands(bot)
    log.info("Bot started.")

@dp.shutdown()
async def on_shutdown():
    log.info("Bot shutting down…")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())