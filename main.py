import logging
from datetime import datetime, timedelta
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states for ConversationHandler
SERVER_SEED, SHOW_RESULT = range(2)

# User usage tracking dictionary
user_usage = {}
shown_images = set()

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    welcome_message = (
        "WELCOME STAKE FREE BOT\n\n"
        "⚠️ WARNING ⚠️\n\n"
        "📗 If Anyone Wants Paid Bot Then Buy From Our Verified Seller. We Are Not Responsible For Where To Buy Otherwise.\n\n"
        "📗 We Will Not Take Responsibility If You Are Scammed If You Buy From Someone Else.\n\n"
        "OUR VERIFIED TEAM ⬇️\n"
        "@Stake_Bot_support\n\n"
        "Payment Gateway ⬇️\n"
        "@Stake_payment_bot\n\n"
        "ONLY PAID OUR VERIFIED USERNAME ✅\n\n"
        "Choose Your Game.. ⏳"
    )
    update.message.reply_text(welcome_message, parse_mode='Markdown')
    show_game_options(update, context)

def show_game_options(update: Update, context: CallbackContext) -> None:
    """Show game options as inline buttons."""
    keyboard = [
        [InlineKeyboardButton("Mines 💎 (FREE)", callback_data='mines')],
        [InlineKeyboardButton("KENO 💵 ($)", callback_data='keno')],
        [InlineKeyboardButton("DICE 🎲 ($)", callback_data='dice')],
        [InlineKeyboardButton("Dragon Tower 🐉 ($)", callback_data='dragon_tower')],
        [InlineKeyboardButton("LIMBO 📉 ($)", callback_data='limbo')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose Your Game:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> int:
    """Handle button presses."""
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    if query.data == 'mines':
        response = (
            "Select which Bot you want 🤖\n\n"
            "INFO ℹ️\n\n"
            "PAID BOT 98.99% ACCURACY 🎯 AND API SUPPORT ⚡\n\n"
            "FREE BOT 85% ACCURACY 🎯 AND NOT API SUPPORT 🚫"
        )
        query.edit_message_text(text=response, parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton("Paid bot 💰", callback_data='paid_bot')],
            [InlineKeyboardButton("Free bot 💎", callback_data='free_bot')],
            [InlineKeyboardButton("Back", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Choose bot type:', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data in ['keno', 'dice', 'dragon_tower', 'limbo']:
        response = (
            "To use this game, you need to buy the paid bot subscription.\n\n"
            "Telegram bot subscription💰\n\n"
            "🍀98% WIN RATE 🍀\n\n"
            "Pay now ✅"
        )
        query.edit_message_text(text=response, parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton("Secured payment 💳", callback_data='payment')],
            [InlineKeyboardButton("Back", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Buy Paid Bot for unlimited access:', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == 'free_bot':
        # Check if user has already used the free bot more than twice in a day
        usage_info = user_usage.get(user_id, {"count": 0, "last_reset": datetime.now()})
        if usage_info["last_reset"] < datetime.now() - timedelta(days=1):
            usage_info = {"count": 0, "last_reset": datetime.now()}

        if usage_info["count"] >= 2:
            response = (
                "⚠️ You have reached the limit of 2 free uses per day. "
                "Please buy the paid bot for unlimited access."
            )
            query.edit_message_text(text=response, parse_mode='Markdown')

            keyboard = [
                [InlineKeyboardButton("Buy Paid Bot 💰", callback_data='paid_bot')],
                [InlineKeyboardButton("Back", callback_data='mines')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Buy Paid Bot for unlimited access:', reply_markup=reply_markup)
        else:
            user_usage[user_id] = {"count": usage_info["count"] + 1, "last_reset": usage_info["last_reset"]}

            response = (
                "⚠️ Attention ⚠️\n\n"
                "🍀 You can use the free version\n\n"
                "🕰 Result show 2 Times in a day\n\n"
                "🎯 82% accuracy in Free version 💎\n\n"
                "🔺 BET SMALL AMOUNT"
            )
            query.edit_message_text(text=response, parse_mode='Markdown')

            keyboard = [
                [InlineKeyboardButton("Select mine 💣", callback_data='select_mine')],
                [InlineKeyboardButton("Back", callback_data='mines')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Select mine 💣', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == 'select_mine':
        response = "Please select the number of mines."
        query.edit_message_text(text=response, parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton("1 💣", callback_data='mine_1')],
            [InlineKeyboardButton("2 💣", callback_data='mine_2')],
            [InlineKeyboardButton("3 💣", callback_data='mine_3')],
            [InlineKeyboardButton("4 💣", callback_data='mine_4')],
            [InlineKeyboardButton("Back", callback_data='free_bot')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Select a mine:', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data in ['mine_1', 'mine_2', 'mine_3', 'mine_4']:
        response = "Find your (Active Server Seed) and paste it here:"
        query.edit_message_text(text=response, parse_mode='Markdown')
        return SERVER_SEED

    elif query.data == 'paid_bot':
        response = (
            "Telegram bot subscription💰\n\n"
            "🍀98% WIN RATE 🍀\n\n"
            "Pay now ✅"
        )
        query.edit_message_text(text=response, parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton("Secured payment 💳", callback_data='payment')],
            [InlineKeyboardButton("Back", callback_data='mines')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('PAY USING UPI', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == 'payment':
        response = (
            "Pay and send screenshot 📸 to @Stake_Bot_support\n\n"
            "Pay now 💵"
        )
        query.edit_message_text(text=response, parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton("Pay now 💵", callback_data='pay_now')],
            [InlineKeyboardButton("Back", callback_data='paid_bot')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('PAY USING UPI', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == 'pay_now':
        response = "Payment done 👍"
        query.edit_message_text(text=response, parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton("Payment Done 😍😍", callback_data='')],
            [InlineKeyboardButton("Main Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Payment done 👍', reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == 'show_result':
        response = "Loading... 🌐"
        query.edit_message_text(text=response, parse_mode='Markdown')

        if len(shown_images) == 28:
            shown_images.clear()

        available_images = set(range(1, 29)) - shown_images
        image_number = random.choice(list(available_images))
        shown_images.add(image_number)
        image_path = os.path.join(f'{image_number}.png')

        keyboard = [
            [InlineKeyboardButton("Main Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.message.reply_photo(photo=open(image_path, 'rb'), reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == 'check_result':
        response = "Loading... 🌐"
        query.edit_message_text(text=response, parse_mode='Markdown')

        if len(shown_images) == 28:
            shown_images.clear()

        available_images = set(range(1, 29)) - shown_images
        image_number = random.choice(list(available_images))
        shown_images.add(image_number)
        image_path = os.path.join(f'{image_number}.png')

        keyboard = [
            [InlineKeyboardButton("Main Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.message.reply_photo(photo=open(image_path, 'rb'), reply_markup=reply_markup)
        return ConversationHandler.END

def handle_server_seed(update: Update, context: CallbackContext) -> int:
    """Handle the server seed input from the user."""
    server_seed = update.message.text
    response = "Server seed received: " + server_seed

    if server_seed:
        response = "Server seed received: " + server_seed
    else:
        response = "Server seed not found. Please enter it again."

    update.message.reply_text(response, parse_mode='Markdown')

    keyboard = [
        [InlineKeyboardButton("Show result", callback_data='show_result')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Show result:', reply_markup=reply_markup)
    return SHOW_RESULT

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message when the command /help is issued."""
    update.message.reply_text('Help! Use /start to begin.')

def main() -> None:
    """Start the bot."""
    updater = Updater("6541537570:AAGlBORq7A2IHiUm3NdEiaRj5ML4LfxVDKU")
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Add conversation handler for handling server seed
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            SERVER_SEED: [MessageHandler(Filters.text & ~Filters.command, handle_server_seed)],
            SHOW_RESULT: [CallbackQueryHandler(button)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


