import json
import logging

from kafka import KafkaProducer
from pydantic import ValidationError
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import Config
from Message import Msg


logger = logging.getLogger(f"youtube2podcast")
youtube_hosts = ['www.youtube.com',
                 'youtube.com',
                 'youtu.be']


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def produce_message(update: Update, context: CallbackContext) -> None:
    c = Config()
    producer = KafkaProducer(bootstrap_servers=c.KAFKA_DSN,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    try:
        msg = Msg(tg_chat_id=update.message.chat.id,
                  tg_message_id=update.message.message_id,
                  user_msg=update.message.text)
        if msg.user_msg.host.lower() not in youtube_hosts:
            print(msg.user_msg.host.lower())
            raise ValidationError
        producer.send('sample', dict(msg))
        #logger.info(f"message was sent: {msg.json()}")
        print(f"message was sent:{dict(msg)}")
    except ValidationError as e:
        logger.error(e)
        update.message.reply_text('Wrong URL')
    # msg = {"tg_chat_id": update.message.chat.id,
    #        "tg_message_id": update.message.message_id,
    #        "user_msg": update.message.text
    #        }


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    c = Config()
    updater = Updater(c.BOT_ACCESS_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, produce_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
