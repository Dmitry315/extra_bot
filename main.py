# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from random import randint, seed
from time import gmtime, strftime
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
skip_key = [['/skip']]
skip_menu = ReplyKeyboardMarkup(skip_key, one_time_keyboard=False)


def start(bot, update):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?", reply_markup=skip_menu)

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения
    # от этого пользователя должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


# Добавили словарь user_data в параметры.
def first_response(bot, update, user_data):
    # Сохраняем ответ в словаре.
    user_data['locality'] = update.message.text
    update.message.reply_text(
        "Какая погода в городе {0}?".format(user_data['locality']))
    return 2


# Добавили словарь user_data в параметры.
def second_response(bot, update, user_data):
    weather = update.message.text
    # Используем user_data в ответе.
    if user_data['locality'] == '':
        update.message.reply_text("Спасибо за участие в опросе!")
    else:
        update.message.reply_text("Спасибо за участие в опросе! Привет, {0}!".format(user_data['locality']))
    return ConversationHandler.END


def skip(bot, update, user_data):
    user_data['locality'] = ''
    update.message.reply_text('Какая погода у вас за окном?')
    return 2



def stop(bot, update):
    update.message.reply_text("Жаль. А было бы интерсно пообщаться. Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.




def main():
    # Создаём объект updater. Вместо слова "TOKEN" надо разместить
    # полученный от @BotFather токен
    updater = Updater(token='804034448:AAEeUxtrNhYJg77TUCy_egsG6BWgMpPfgWM')
    conv_handler = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start', start)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text, first_response, pass_user_data=True), CommandHandler('skip', skip, pass_user_data=True)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text, second_response, pass_user_data=True)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )
    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("skip", skip))

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()