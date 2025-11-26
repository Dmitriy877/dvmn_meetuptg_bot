import logging

from django.core.management.base import BaseCommand

from meetbot.bot import run_bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запускает Telegram-бот (long polling)'

    def handle(self, *args, **options):
        try:
            run_bot()
        except Exception:
            logger.exception('Bot crashed')
            raise
