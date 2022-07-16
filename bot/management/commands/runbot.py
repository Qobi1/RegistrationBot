from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from django.core.management import BaseCommand
from bot.views import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        TOKEN = ""
        updater = Updater(TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, received_message))
        updater.dispatcher.add_handler(MessageHandler(Filters.document, received_file))
        updater.dispatcher.add_handler(MessageHandler(Filters.contact, received_contact))
        updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))
        updater.start_polling()
        updater.idle()