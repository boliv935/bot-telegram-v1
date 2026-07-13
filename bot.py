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
MENU_IMAGE_URL = "https://i.ibb.co/Mxq7cQ0s/Gemini-Generated-Image-9necwx9necwx9nec.png"   # Image du menu catalogue (image_4.png)

# --- 1. FONCTION DE RÉUTILISATION DU MENU PRINCIPAL ---
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Contact+Information 🇫🇷 💵", callback_data="menu_contact")
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
        "⚪ **WhatsApp**: [+33746407167](https://wa.me/33746407167?text=Hello%20Cali%20Gas%2093%20!%20C'est%20mon%20premier%20contact%20.%0A%0A%F0%9F%94%92%20PROFIL%20CLIENT%20%3A%0A*%20Mon%20Pr%C3%A9nom%20%2F%20Pseudo%20%3A%20%5B%20...%20%5D%0A*%20%C3%82ge%20%3A%20%5B%20...%20%5D%0A*%20Ville%20%2F%20Zone%20actuelle%20%3A%20%5B%20Ex%3A%20Paris%2018%20%2F%20Bondy%20Sud%20%5D%0A%0AJe%20suis%20int%C3%A9ress%C3%A9%20par%20%3A)\n"
        "⚪ **More Info**: Linktr.ee/CaliGas99\n\n"
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
        caption="Bienvenue dans la Gas Station⛽⚡!",
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
        caption="Bienvenue dans la Gas Station⛽⚡!",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

# --- 7. LES FICHES PRODUITS (Chacune intègre le bouton Retour) ---
@dp.callback_query(F.data == "menu_contact")
async def process_contact(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = (
        "**CONTACT + PAYMENT INFO** 🇪🇺 💵\n\n"
         " • Canal POTATO: \n"
         " • Canal Telegram: \n"
         " • Canal MEET-UP: \n"
        "**Comment nous contactez ?** 📱:\n"
        "• Telegram: @Caligass\n"
        "• WhatsApp: +33746407167\n"
        "• Signal: @Caligass\n"
        "**PAYMENT METHODS**:\n"
        "-PAIEMENT EN ESPÈCE💵\n-BTC\n"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu") # Bouton Retour
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_cali")
async def process_cali(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = "**CALI SPAIN🇪🇸🇺🇸**\nAU MEET-UP🏠\n•1,2g = 10€\n• 10g = 90€\nEN LIVRAISON🛵🛴\n\n•3,5g = 30€\n• 6,5g = 50€\nPrise de commande📲:\n[WhatsApp☎️](https://wa.me/<33746407167>)  "
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu")
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_spanish")
async def process_spanish(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = "**Amnésia Haze🇪🇸**\n AU MEET-UP🏠n\n 1g = 5€\n• 7g = 30€\n\nEN LIVRAISON🛵🛴\n\n•1,2g = 10€\n• 10g = 130€\n\nPrise de commande📲:\n[WhatsApp☎️](https://wa.me/<33746407167>)"
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="go_to_menu")
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "menu_hash")
async def process_hash(callback: types.CallbackQuery):
    await callback.message.delete()
    
    text = "**TOP MOUSSEUX🇲🇦**\nAU MEET-UP🏠n\n• 2g = 5€\n• 4g = 10€\n\nEN LIVRAISON🛵🛴\n\n•1,2g = 10€\n• 10g = 130€\n\nPrise de commande📲:\n[WhatsApp☎️](https://wa.me/<33746407167>)"
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
