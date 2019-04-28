# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from random import randint, seed
from time import gmtime, strftime
import json

seed()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
main_keys = [['/dice'], ['/timer']]
main_menu = ReplyKeyboardMarkup(main_keys, one_time_keyboard=False)

dice_keys = [['кинуть один шестигранный кубик',
'кинуть 2 шестигранных кубика одновременно'],
['кинуть 20-гранный кубик',
'вернуться назад']]
dice_menu = ReplyKeyboardMarkup(dice_keys, one_time_keyboard=False)

timer_keys = [['30 секунд',
'1 минута'],
['5 минут',
'вернуться назад']]
timer_menu = ReplyKeyboardMarkup(timer_keys, one_time_keyboard=False)

wait_key = [['/close']]
wait_menu = ReplyKeyboardMarkup(wait_key , one_time_keyboard=False)

def start(bot, update):
    update.message.reply_text("Я бот-помощник для игр. Что вам нужно?", reply_markup=main_menu)

def dice(bot, update):
    update.message.reply_text("Какой кубик кинуть?", reply_markup=dice_menu)

def timer(bot, update):
    update.message.reply_text("Сколько засечь?", reply_markup=timer_menu)

def close(bot, update, chat_data):
    if 'job' in chat_data:
        # планируем удаление задачи (выполнется, когда будет возможность)
        chat_data['job'].schedule_removal()
        # и очищаем пользовательские данные
        del chat_data['job']

    update.message.reply_text('Хорошо, вернулся сейчас!', reply_markup=timer_menu)

def task_30_sec(bot, job):
    bot.send_message(job.context, text='30 секунд истекло', reply_markup=timer_menu)
def task_1_min(bot, job):
    bot.send_message(job.context, text='1 минута истекла', reply_markup=timer_menu)
def task_5_min(bot, job):
    bot.send_message(job.context, text='5 минут истекло', reply_markup=timer_menu)

def parser(bot, update, job_queue, chat_data):
    text = update.message.text
    if text == 'кинуть один шестигранный кубик':
        update.message.reply_text('Выпало: ' + str(randint(1, 6)), reply_markup=dice_menu)
    elif text == 'кинуть 2 шестигранных кубика одновременно':
        update.message.reply_text('Выпало: ' + str(randint(1, 6)) + ' и ' + str(randint(1, 7)), reply_markup=dice_menu)
    elif text == 'кинуть 20-гранный кубик':
        update.message.reply_text('Выпало: ' + str(randint(1, 20)), reply_markup=dice_menu)

    elif text == '30 секунд':
        delay = 30
        update.message.reply_text('засек 30 секунд', reply_markup=wait_menu)
        job = job_queue.run_once(task_30_sec, delay, context=update.message.chat_id)
        chat_data['job'] = job
    elif text == '1 минута':
        delay = 60
        update.message.reply_text('засек 1 минуту', reply_markup=wait_menu)
        job = job_queue.run_once(task_1_min, delay, context=update.message.chat_id)
        chat_data['job'] = job
    elif text == '5 минут':
        delay = 300
        update.message.reply_text('засек 5 минут', reply_markup=wait_menu)
        job = job_queue.run_once(task_5_min, delay, context=update.message.chat_id)
        chat_data['job'] = job

    elif text == 'вернуться назад':
        update.message.reply_text('Что от меня требуется?', reply_markup=main_menu)


def main():
    # Создаём объект updater. Вместо слова "TOKEN" надо разместить
    # полученный от @BotFather токен
    updater = Updater(token='804034448:AAEeUxtrNhYJg77TUCy_egsG6BWgMpPfgWM')

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher


    text_handler = MessageHandler(Filters.text, parser, pass_job_queue=True, pass_chat_data=True)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("close", close, pass_chat_data=True))

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()