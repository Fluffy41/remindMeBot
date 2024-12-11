import telegram
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telegram.Bot(token="1185647707:AAEt_96YZYd3-FRbEbDeLDaFKtEqtczmVA4")

data = {}


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! what reminder do you need?\n\n" +
                                                                    "Use /put to create new reminders.\n" +
                                                                    "e.g. /put clear laundry")


start_handler = CommandHandler("start", start)


# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

def put(update, context):
    user_input = update.message.text
    try:
        cache_message = user_input.partition(" ")[2]
        if cache_message == "":
            context.bot.send_message(chat_id=update.effective_chat.id, text="Not a valid reminder!")
        else:
            data["key"] = cache_message
            context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, when do you want it?\n\n" +
                                                                            "Use /set to set timer" +
                                                                            " in this format: 5w 2d 3h 20m 3s\n"
                                                                            "e.g. /set 30s or /set 1hr 30min")
    except (IndexError, ValueError):
        update.message.reply_text("Use /put to create new reminders.\n" +
                                  "e.g. /put clear laundry")


put_handler = CommandHandler("put", put)


def set(update, context):
    try:
        user_input = update.message.text
        if isValid(user_input.split()):
            time_set = user_input.split()[1:]
            time_in_seconds = seconds(time_set)
            context.job_queue.run_once(call_back_time, time_in_seconds, context=update.message.chat_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Reminder set successfully!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Not a valid time!")
    except (IndexError, ValueError):
        update.message.reply_text("Use /set to set when you want to be reminded" +
                                  " in this format: 5w 2d 3h 20m 3s\n "
                                  "e.g. /set 30s or /set 1hr 30min")


set_handler = CommandHandler("set", set)


def isValid(time_list):
    for time in time_list:
        if len(time) > 1:
            unit = time[len(time) - 1]
            number = time[:len(time) - 1]
            if unit == 'w' or unit == 'd' or unit == 'h' or unit == 'm' or unit == 's':
                if str.isdigit(number):
                    return True
    return False


def seconds(time_list):
    time_in_seconds = 0
    for time in time_list:
        if 'w' in time:
            time_in_seconds += (int(time[:len(time) - 1]) * 604800)
        elif 'd' in time:
            time_in_seconds += (int(time[:len(time) - 1]) * 86400)
        elif 'h' in time:
            time_in_seconds += (int(time[:len(time) - 1]) * 3600)
        elif 'm' in time:
            time_in_seconds += (int(time[:len(time) - 1]) * 60)
        else:
            time_in_seconds += int(time[:len(time) - 1])
    return time_in_seconds


def call_back_time(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text=data["key"])


def main():
    # Create the application
    application = Application.builder().token("1185647707:AAEt_96YZYd3-FRbEbDeLDaFKtEqtczmVA4").build()

    # Add Handlers
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
