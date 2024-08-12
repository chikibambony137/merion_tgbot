from telebot import TeleBot, types
import config, messages, jokes as j
import random
from io import StringIO

bot = TeleBot(config.token) # creating new object "bot" of class "Telebot" with argument token from BotFather

@bot.message_handler(commands=['start']) # decorator for new functional of handling message to my function (/start)
def send_start_message(message: types.Message):
    """Send start message with hello-words
    """
    bot.send_message(message.chat.id, messages.start_message)

@bot.message_handler(commands=['help']) # /help
def send_help_message(message: types.Message):
    """Send all avaiable bot commands
    """
    bot.send_message(message.chat.id, messages.help_message)

@bot.message_handler(commands=['joke']) # /joke
def send_random_joke(message: types.Message):
    """Send random joke from jokes.jokes: list
    """
    bot.send_message(message.chat.id, random.choice(j.jokes))

@bot.message_handler(commands=['cat'])
def send_cat_on_watermelon(message: types.Message):
    """Send image with cat on watermelon
    """
    bot.send_photo(chat_id=message.chat.id, photo=config.image)

@bot.message_handler(commands=['cat_file'])
def send_doc_cat_on_watermelon(message: types.Message):
    """Send document with cat on watermelon
    """
    bot.send_document(chat_id=message.chat.id, document=config.image)

@bot.message_handler(commands=['me'])
def send_user_info(message: types.Message):
    """Send users info in txt file
    """
    file = StringIO(str(message.from_user)) # writing info from users message to txt file
    file.seek(0) # перенос строки в начало, чтобы потом дописывать файл (конкретно здесь пока нахуй не нада)
    file = types.InputFile(file) # type to send file in telegram

    bot.send_document(chat_id=message.chat.id, 
                      document=file, 
                      visible_file_name='your-info.txt',
                      caption=messages.caption_user_info)

@bot.message_handler() # other message or command
def echo_message(message: types.Message):
    """Communicate with user. With unknown command or message send echo-message
    """
    text = message.text
    text_lower = text.lower()
    if 'привет' in text_lower:
        text = 'И тебе привет!'
    elif 'как дела' in text_lower:
        text = 'Хорошо! А у Вас как?'
    elif any(word in text_lower for word in ['пока', 'до свидания']): # fast-cycle for any word from list in message
        text = 'До новых встреч!'
    bot.send_message(message.chat.id, text)

bot.infinity_polling(skip_pending=True) # Infinity cycle for handling users messages, 
                                        # skip_pending - ignore "waiting" messages (disable before global launch)