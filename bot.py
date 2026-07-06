import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# Clé API de votre bot (Gérée sur Render)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ------------------------------------------------------------------
# ⚙️ CONFIGURATION PERSONNELLE (Modifiez ce qui est entre guillemets)
# ------------------------------------------------------------------

# 1. Vos mots pour le Captcha de sécurité
CAPTCHA_WORDS = ["static", "dry", "frozen", "mousse"]

# 2. Vos contacts officiels
TELEGRAM_CONTACT = "@VotrePseudoTelegram"  # Mettez votre vrai @ d'utilisateur
THREEMA_ID = "377Z6UAA"                    # Mettez votre ID Threema ou supprimez la ligne

# 3. Liens de vos photos (Remplacez par les URL de vos propres images)
URL_PHOTO_ACCUEIL = "https://picsum.photos/500/500?random=10"  # Image après le captcha
URL_PHOTO_CALI    = "https://picsum.photos/500/500?random=11"  # Image pour la Cali
URL_PHOTO_SPANISH = "https://picsum.photos/500/500?random=12"  # Image pour la Spanish
URL_PHOTO_HASH    = "https://picsum.photos/500/500?random=13"  # Image pour le Hash

# ------------------------------------------------------------------

# Déclenchement du Captcha (/start)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    correct_word = random.choice(CAPTCHA_WORDS)
    buttons_words = CAPTCHA_WORDS.copy()
    random.shuffle(buttons_words)
    
    text = f"Prove you are not a robot.\n\nClick the bolded word:\n👉 **{correct_word}** 👈"
    builder = InlineKeyboardBuilder()
    for word in buttons_words:
        callback_data = "captcha_good" if word == correct_word else "captcha_bad"
        builder.button(text=word, callback_data=callback_data)
    
    builder.adjust(2)
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data == "captcha_bad")
async def process_bad_captcha(callback: types.CallbackQuery):
    await callback.answer("❌ Mauvais choix ! Réessayez avec /start", show_alert=True)

# Menu Principal après réussite du Captcha
@dp.callback_query(F.data == "captcha_good")
async def process_good_captcha(callback: types.CallbackQuery):
    await callback.message.delete()
    
    builder = InlineKeyboardBuilder()
    # Modifiez ici le texte visible sur les boutons si besoin
    builder.button(text="Contact + Infos Payment Information 🇫🇷 💵", callback_data="menu_contact")
    builder.button(text="Cali Flower 🇺🇸 Stock in Europe 🇪🇺", callback_data="menu_cali")
    builder.button(text="Spanish Flower 🇪🇸 Stock in Europe 🇪🇺", callback_data="menu_spanish")
    builder.button(text="Hash / Dry Stock in Europe 🇪🇺", callback_data="menu_hash")
    builder.adjust(1)
    
    await callback.message.answer_photo(
        photo=URL_PHOTO_ACCUEIL,
        caption="Bienvenue dans la GAS STATION by CALI GAS⛽ ! Choose an option below:",
        reply_markup=builder.as_markup()
    )

# Bouton : CONTACT & PAIEMENT
@dp.callback_query(F.data == "menu_contact")
async def process_contact(callback: types.CallbackQuery):
    text = (
        "**CONTACT + PAYMENT INFO** 🇪🇺 💵\n\n"
        "**Nous contactez** 📱:\n"
        f"• Telegram: {TELEGRAM_CONTACT}\n"
        f"• Threema: {THREEMA_ID}\n\n"
        "**IMPORTANT READ BEFORE ORDER**:\n"
        "• Landing rate is 99% from Spain 🇪🇸 / Europe Shipping 🇪🇺\n"
        "• No reship, only if you pay insurance\n\n"
        "**PAYMENT METHODS**:\n"
        "- CRYPTO: BTC, USDT, LTC\n"
        "- CPP (Cash Per Post)\n"
        "- CASH DROPS IN EUROPE 🇪🇺"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

# Bouton : CALI FLOWER
@dp.callback_query(F.data == "menu_cali")
async def process_cali(callback: types.CallbackQuery):
    text = (
        "**CALI FLOWER 🇺🇸**\n"
        "Stock disponible en Europe (Livraison rapide) 🇪🇺\n\n"
        "**TARIFS :**\n"
        "• 5g : 70€\n"
        "• 10g : 130€\n"
        "• 50g : 500€\n\n"
        f"👉 Pour commander, contactez : {TELEGRAM_CONTACT}"
    )
    await callback.message.answer_photo(photo=URL_PHOTO_CALI, caption=text, parse_mode="Markdown")
    await callback.answer()

# Bouton : SPANISH FLOWER
@dp.callback_query(F.data == "menu_spanish")
async def process_spanish(callback: types.CallbackQuery):
    text = (
        "**SPANISH FLOWER 🇪🇸**\n"
        "Stock direct de Catalogne ☀️\n\n"
        "**TARIFS :**\n"
        "• 10g : 80€\n"
        "• 50g : 300€\n"
        "• 100g : 550€\n\n"
        f"👉 Pour commander, contactez : {TELEGRAM_CONTACT}"
    )
    await callback.message.answer_photo(photo=URL_PHOTO_SPANISH, caption=text, parse_mode="Markdown")
    await callback.answer()

# Bouton : HASH / DRY
@dp.callback_query(F.data == "menu_hash")
async def process_hash(callback: types.CallbackQuery):
    text = (
        "**HASH / DRY SIFT 🇪🇺**\n"
        "Le meilleur du hash filtré en stock.\n\n"
        "**TARIFS :**\n"
        "• 10g : 90€\n"
        "• 50g : 350€\n"
        "• 100g : 600€\n\n"
        f"👉 Pour commander, contactez : {TELEGRAM_CONTACT}"
    )
    await callback.message.answer_photo(photo=URL_PHOTO_HASH, caption=text, parse_mode="Markdown")
    await callback.answer()

# Serveur Web de maintien pour Render Free
async def handle(request):
    return web.Response(text="Bot runs successfully!")

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
