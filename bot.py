import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from playwright.async_api import async_playwright
import asyncio

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

# Crear la aplicación
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scrape", scrape))

# Ejecutar el bot (Render ya maneja el event loop)
app.run_polling()
