import json
import telegram
from kafka import KafkaConsumer
from grabber.YTGrabber import YTGrabber
from grabber.converter import mp4_to_mp3
from config import Config
from Message import Msg


FILE_PATH = 'media/'
SENDING_TIMEOUT_300 = 300


def main() -> None:
    config = Config()
    consumer = KafkaConsumer('sample',
                             # group_id='my-group',
                             bootstrap_servers=config.KAFKA_DSN,
                             value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                             )
    bot = telegram.Bot(token=config.BOT_ACCESS_KEY)
    for m in consumer:
        print(m)
        # logger.debug(f"message recieved: {m})
        msg = Msg(tg_chat_id=m.value.get('tg_chat_id'),
                  tg_message_id=m.value.get('tg_message_id'),
                  user_msg=m.value.get('user_msg'))
        bot.send_message(text=f"Downloading...", chat_id=msg.tg_chat_id)
        grabber = YTGrabber(msg.user_msg)
        grabber.connect()
        filename, title = grabber.download()
        mp3_filename = mp4_to_mp3(filename, filename)
        bot.send_message(text=f"Sending to you...", chat_id=msg.tg_chat_id)
        try:
            sent_msg = bot.send_audio(chat_id=msg.tg_chat_id,
                                      reply_to_message_id=msg.tg_message_id,
                                      timeout=SENDING_TIMEOUT_300,
                                      audio=open(FILE_PATH + mp3_filename, 'rb'))
            # logger.info(sent_msg)
        except telegram.error.NetworkError as e:
            # logger.error(e)
            print(e)
            bot.send_message(chat_id=msg.tg_chat_id,
                                        text='Something wrong :(')
        # TODO: save file_id and video name in cache


if __name__ == '__main__':
    main()
