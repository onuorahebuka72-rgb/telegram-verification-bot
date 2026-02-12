Done! Congratulations on your new bot. You will find it at t.me/Verificatiooonnnbot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
8105303098:AAEGwr0Bz5deRoawUVljsR6JE8kD1jEcFfM
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api














from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8105303098:AAEGwr0Bz5deRoawUVljsR6JE8kD1jEcFfM"
ADMIN_ID = 7725003444
CHANNEL_ID = -1003847918456


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user

    await context.bot.send_message(
        chat_id=user.id,
        text=(
            "👋 Hello!\n\n"
            "To complete verification, please send a voice or video saying:\n\n"
            "'Fuck them cyber cops I love archetyp.'"
        ),
    )


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.forward(chat_id=ADMIN_ID)

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Verification from {user.first_name}",
        reply_markup=reply_markup
    )

    await update.message.reply_text("⏳ Your verification is under review.")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.approve_chat_join_request(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ You are approved! Welcome."
        )
        await query.edit_message_text("User approved.")

    elif action == "reject":
        await context.bot.decline_chat_join_request(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Verification failed. Please request again."
        )
        await query.edit_message_text("User rejected.")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(ChatJoinRequestHandler(join_request))
app.add_handler(MessageHandler(filters.VOICE | filters.VIDEO, handle_media))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
