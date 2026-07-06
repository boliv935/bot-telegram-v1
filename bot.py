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

# Liste des mots du captcha
CAPTCHA_WORDS = ["static", "dry", "frozen", "mousse"]

# Liens d'images (Remplacez par vos propres URL directes de photos)
LOGO_WELCOME_URL = "https://i.ibb.co/DTJRnM7/Gemini-Generated-Image-5q51bn5q51bn5q51.png" # Image d'accueil (image_2.png)
MENU_IMAGE_URL = "https://picsum.photos/500/500?random=2"   # Image du menu catalogue (image_4.png)

# --- 1. FONCTION DE RÉUTILISATION DU MENU PRINCIPAL ---
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Contact 🇫🇷 💵", callback_data="menu_contact")
    builder.button(text="Cali US / Cali Spain 🇺🇸🇪🇸", callback_data="menu_cali")
    builder.button(text="TOP Haze 🇳🇱 ! ", callback_data="menu_spanish")
    builder.button(text="Hash / Dry🇲🇦🇺🇸", callback_data="menu_hash")
    builder.adjust(1) # 1 bouton par ligne
    return builder.as_markup()

# --- 2. ACCUEIL PRINCIPAL (Dès que l'utilisateur fait /start) ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Access Menu 📋", callback_data="trigger_captcha")
    
    welcome_text = (
        "🇫🇷 **GAS STATION By CALI GAS⛽ ** 🌐\n\n"
        "⚪ **Telegram**: @Caligass\n"
        "⚪ **WhatsApp**: 377Z6UAA\n"
        "⚪ **More Info**: Linktr.ee/votrelien\n\n"
        "📱 **MENU TOUJOUR A JOUR ✔️!**\n"
        "📝"
    )
    await message.answer_photo(
        photo=LOGO_WELCOME_URL,
        caption=welcome_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# --- 3. LANCEMENT DU CAPTCHA (Après clic sur "Access the Menu 📋") ---
@dp.callback_query(F.data == "trigger_captcha")
async def start_captcha(callback: types.CallbackQuery):
    await callback.message.delete() # On efface l'accueil pour afficher le captcha
    
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

# --- 4. GESTION DU MAUVAIS MOT ---
@dp.callback_query(F.data == "captcha_bad")
async def process_bad_captcha(callback: types.CallbackQuery):
    await callback.answer("❌ Mauvais choix ! Réessayez avec /start", show_alert=True)

# --- 5. GESTION DU BON MOT (Affichage de la vitrine catalogue) ---
@dp.callback_query(F.data == "captcha_good")
async def process_good_captcha(callback: types.CallbackQuery):
    await callback.message.delete() # On efface le captcha réussi
    
    await callback.message.answer_photo(
        photo=MENU_IMAGE_URL,
        caption="Welcome to the Official Menu! Choose an option below:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

# --- 6. ACTION DU BOUTON RETOUR (Revient à la vitrine catalogue) ---
@dp.callback_query(F.data == "go_to_menu")
async def process_back_to_menu(callback: types.CallbackQuery):
    await callback.message.delete() # Supprime la fiche produit actuelle
    
    # Renvoie le menu catalogue proprement
    await callback.message.answer_photo(
        photo=MENU_IMAGE_URL,
        caption="Welcome to the Official Menu! Choose an option below:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

# --- 7. LES FICHES PRODUITS (Chacune intègre le bouton Retour) ---
@dp.callback_query(F.data == "menu_contact")
async def process_contact(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = (
        "**CONTACT + PAYMENT INFO** 🇪🇺 💵\n\n"
        "**HOW TO CONTACT** 📱:\n"
        "• Telegram: @VotreContactPlug\n\n"
        "**PAYMENT METHODS**:\n"
        "- CRYPTO: BTC, USDT, LTC\n"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu") # Bouton Retour
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_cali")
async def process_cali(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = "**CALI FLOWER 🇺🇸**\n\n• 5g = 70€\n• 10g = 130€"
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu")
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_spanish")
async def process_spanish(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = "**SPANISH FLOWER 🇪🇸**\n\n• 10g = 80€\n• 50g = 300€"
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu")
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_hash")
async def process_hash(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = "**HASH / DRY SIFT 🇪🇺**\n\n• 10g = 90€\n• 50g = 350€"
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu")
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()


# --- 8. SERVEUR WEB POUR RENDER FREE ---
async def handle(request):
    return web.Response(text="Bot is running!")

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
