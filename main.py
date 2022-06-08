from telebot.async_telebot import AsyncTeleBot
import asyncio
import hangman

# hangman_jb_bot
bot = AsyncTeleBot('5555940265:AAEmwnqA6OJHwfkOcYb6wdkZ6hWQVMtpc7w')

GREET_TEXT = 'H A N G M A N'

games = {}


def greet_user(message):
    greeting = GREET_TEXT + '\n' + 'Привет, {}!'.format(message.from_user.first_name)
    games[message.chat.id] = hangman.Hangman(message.chat.id)
    reply = games[message.chat.id].proceed('')
    return bot.send_message(message.chat.id, greeting + '\n' + reply)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await greet_user(message)


def user_input_callback(message):
    if message.chat.id in games:
        reply = games[message.chat.id].proceed(message.text)
        if reply == hangman.BYE_TEXT:
            del games[message.chat.id]
    else:
        reply = 'Enter /start first!'
    return bot.send_message(message.chat.id, reply)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True, content_types=['text'])
async def user_input(message):
    await user_input_callback(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = 0

    try:
        task = asyncio.ensure_future(bot.polling())
        result = loop.run_until_complete(task)
    except KeyboardInterrupt:
        if task:
            task.cancel()
            loop.stop()
        print('exiting')
    finally:
        if result:
            exit(result)
        else:
            exit(0)
