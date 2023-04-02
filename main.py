import logging
import openai
from decouple import config
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize OpenAI API
openai.api_key = config('OPENAI_API_KEY')
telegram_token = config('TELEGRAM_BOT_TOKEN')

# Define a function to handle /start command
def start_handler(update, context):
    # Send a welcome message and a keyboard menu
    keyboard = [['Chat', 'Help'], ['Cancel']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi there! How can I assist you today?', reply_markup=reply_markup)

# Define a function to handle /help command
def help_handler(update, context):
    # Send a help message
    context.bot.send_message(chat_id=update.effective_chat.id, text='How can I help you?')

# Define a function to handle /cancel command
def cancel_handler(update, context):
    # Send a cancel message and hide the keyboard
    context.bot.send_message(chat_id=update.effective_chat.id, text='Okay, let me know if you need anything else.', reply_markup=telegram.ReplyKeyboardRemove())

# Define a function to handle incoming messages
def message_handler(update, context):
    # Get the message from the user
    message = update.message.text

    # Generate a response using OpenAI API
    response = openai.Completion.create(engine="text-davinci-003", prompt=message, max_tokens=1000, n=1, stop=None, temperature=0.5)
    response_text = response.choices[0].text

    # Send the response back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

# Define a function to handle inline keyboard button presses
def button_handler(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'chat':
        # Send a chat message and hide the keyboard
        context.bot.send_message(chat_id=query.message.chat_id, text='Коротко. Що ти можеш? Українською.', reply_markup=telegram.ReplyKeyboardRemove())
    elif query.data == 'help':
        # Send a help message and hide the keyboard
        context.bot.send_message(chat_id=query.message.chat_id, text='Зпитай, чим ти можеш допомогти. Українською.', reply_markup=telegram.ReplyKeyboardRemove())

# Set up the bot and start polling for messages
def main():
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('cancel', cancel_handler))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    # Register inline keyboard handler
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()