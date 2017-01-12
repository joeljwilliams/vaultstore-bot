#!/usr/bin/env python
# vim: ts=2 et sw=2 sts=2 :

from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, Filters
import logging
import config
import os.path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# extensions of accepted audio files that will be stored
accepted_ext = ['.aac', '.3gpp', '.m4a', '.mp3',]

# custom filter for documents with audio extensions specified above
class AudioDocument(BaseFilter):
  def filter(self, message):
    if message.document:
      _, file_ext = os.path.splitext(message.document.file_name)
      return file_ext in accepted_ext
    return False

def start(bot, update):
  bot.sendMessage(update.message.chat_id, text='Bot started')

# method to store (forward) voice notes to specified channel
def storevn(bot, update):
  bot.forwardMessage(config.VNCHAN, update.message.chat_id, update.message.message_id)

def error(bot, update, error):
  logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
  update = Updater(config.TOKEN)
  dp = update.dispatcher

  dp.add_handler(CommandHandler("start", start))
  
  audio_doc = AudioDocument()

  dp.add_handler(MessageHandler(Filters.voice | Filters.audio | audio_doc, storevn))

  dp.add_error_handler(error)

  update.start_polling()

  update.idle()

if __name__ == '__main__':
  main()
