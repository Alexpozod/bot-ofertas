import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from playwright.async_api import async_playwright

# Obtener el token de las variables de entorno de Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Falta el token de Telegram. Define TELEGRAM_TOKEN en Render.")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot iniciado correctamente ✅")

# /scrape
async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Iniciando scraping con Playwright... ⏳")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://example.com")
            title = await page.title()
            await update.message.reply_text(f"Título de la página: {title}")
            await browser.close()
    except Exception as e:
        await update.message.reply_text(f"Error al hacer scraping: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # --- Diagnóstico de conexión ---
    import asyncio
    async def check_connection():
        try:
            me = await app.bot.get_me()
            print(f"✅ Conexión exitosa con la API de Telegram como {me.username}")
        except Exception as e:
            print(f"❌ Error de conexión con Telegram: {e}")

    asyncio.run(check_connection())
    # --- Fin diagnóstico ---

    # Añadir los manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scrape", scrape))

    print("🤖 Bot ejecutándose...")
    app.run_polling()
