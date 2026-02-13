import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv(8105303098:AAEGwr0Bz5deRoawUVljsR6JE8kD1jEcFfM)
ADMIN_ID = 7725003444
CHANNEL_ID = -1003847918456

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in Railway variables")

async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text="👋 Send a voice or video for verification."
        )
    except Exception as e:
        logging.error(e)

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    user = update.message.from_user

    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
    ]]

    try:
        await update.message.forward(chat_id=ADMIN_ID)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Verification from {user.first_name} ({user.id})",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await update.message.reply_text("⏳ Under review.")
    except Exception as e:
        logging.error(e)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    try:
        if action == "approve":
            await context.bot.approve_chat_join_request(
                chat_id=CHANNEL_ID,
                user_id=user_id
            )
            await context.bot.send_message(user_id, "✅ Approved.")
            await query.edit_message_text("Approved.")

        elif action == "reject":
            await context.bot.decline_chat_join_request(
                chat_id=CHANNEL_ID,
                user_id=user_id
            )
            await context.bot.send_message(user_id, "❌ Rejected.")
            await query.edit_message_text("Rejected.")
    except Exception as e:
        logging.error(e)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(ChatJoinRequestHandler(join_request))
app.add_handler(MessageHandler(filters.VOICE | filters.VIDEO, handle_media))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()app.run_polling()    main()app.run_polling()
