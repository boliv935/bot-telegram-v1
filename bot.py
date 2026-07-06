import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

CAPTCHA_WORDS = ["static", "dry", "frozen", "mousse"]
MENU_IMAGE_URL = "https://picsum.photos/500/500"  # Image du catalogue de produits

# Mettez ici le lien internet direct de votre logo (comme sur image_2.png)
LOGO_WELCOME_URL = "https://picsum.photos/500/500" 

# 1. Dès que l'utilisateur fait /start -> On affiche l'image_2.png
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Construction du bouton unique sous la présentation
    builder = InlineKeyboardBuilder()
    builder.button(text="Access the Menu 📋", callback_data="trigger_captcha")
    
    # Texte de présentation identique à l'image_2.png
    welcome_text = (
        "🇪🇸 **FILTERED KINGS MENU OFFICIAL** 🌐\n\n"
        "⚪ **Telegram**: @VotreContactPlug\n"
        "⚪ **Threema**: 377Z6UAA\n"
        "⚪ **More Info**: Linktr.ee/votrelien\n\n"
        "📱 **MENU ALWAYS UP TO DATE!**\n"
        "📝"
    )
    
    await message.answer_photo(
        photo=LOGO_WELCOME_URL,
        caption=welcome_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# 2. Quand l'utilisateur clique sur "Access the Menu 📋" -> On lance le Captcha
@dp.callback_query(F.data == "trigger_captcha")
async def start_captcha(callback: types.CallbackQuery):
    # Optionnel : supprime le message de bienvenue pour nettoyer le chat
    await callback.message.delete()
    
    correct_word = random.choice(CAPTCHA_WORDS)
    buttons_words = CAPTCHA_WORDS.copy()
    random.shuffle(buttons_words)
    
    text = f"Prove you are not a robot.\n\nClick the bolded word:\n👉 **{correct_word}** 👈"
    
    builder = InlineKeyboardBuilder()
    for word in buttons_words:
        callback_data = "captcha_good" if word == correct_word else "captcha_bad"
        builder.button(text=word, callback_data=callback_data)
    
    builder.adjust(2)
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

# 3. Mauvais mot cliqué
@dp.callback_query(F.data == "captcha_bad")
async def process_bad_captcha(callback: types.CallbackQuery):
    await callback.answer("❌ Mauvais choix ! Réessayez avec /start", show_alert=True)

# 4. Bon mot cliqué -> On affiche la vitrine de produits
@dp.callback_query(F.data == "captcha_good")
async def process_good_captcha(callback: types.CallbackQuery):
    await callback.message.delete()
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Contact + Payment Information 🇪🇸 💵", callback_data="menu_contact")
    builder.button(text="Cali Flower 🇺🇸 Stock in Europe 🇪🇺", callback_data="menu_cali")
    builder.button(text="Spanish Flower 🇪🇸 Stock in Europe 🇪🇺", callback_data="menu_spanish")
    builder.button(text="Hash / Dry Stock in Europe 🇪🇺", callback_data="menu_hash")
    builder.adjust(1)
    
    await callback.message.answer_photo(
        photo=MENU_IMAGE_URL,
        caption="Welcome to the Official Menu! Choose an option below:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "menu_contact")
async def process_contact(callback: types.CallbackQuery):
    contact_text = (
        "**CONTACT + PAYMENT INFO** 🇪🇺 💵\n\n"
        "**HOW TO CONTACT** 📱:\n"
        "• Telegram: @VotreContactPlug\n\n"
        "**PAYMENT METHODS**:\n"
        "- CRYPTO: BTC, USDT, LTC\n"
    )
    await callback.message.answer(contact_text, parse_mode="Markdown")
    await callback.answer()

# Serveur web pour l'offre Render Free
async def handle(request):
    return web.Response(text="Bot runs perfectly!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
