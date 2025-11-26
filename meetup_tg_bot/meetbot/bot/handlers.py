import logging
from typing import Final

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

CALLBACK_PROGRAM: Final = 'menu_program'
CALLBACK_QUESTION: Final = 'menu_question'
CALLBACK_NETWORKING: Final = 'menu_networking'
CALLBACK_DONATE: Final = 'menu_donate'
CALLBACK_SUBSCRIBE: Final = 'menu_subscribe'


def _menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton('📅 Программа', callback_data=CALLBACK_PROGRAM),
            InlineKeyboardButton('❓ Вопрос спикеру', callback_data=CALLBACK_QUESTION),
        ],
        [
            InlineKeyboardButton('🤝 Познакомиться', callback_data=CALLBACK_NETWORKING),
            InlineKeyboardButton('🍕 Донат', callback_data=CALLBACK_DONATE),
        ],
        [InlineKeyboardButton('🔔 Подписка', callback_data=CALLBACK_SUBSCRIBE)],
    ]
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    text = (
        'Привет! Я бот Python Meetup.\n'
        '• Задавайте вопросы спикерам во время доклада\n'
        '• Смотрите программу и что идет дальше\n'
        '• Познакомьтесь с участниками и поддержите митап донатом'
    )

    if update.message:
        await update.message.reply_text(text, reply_markup=_menu_keyboard())
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=_menu_keyboard())


async def handle_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    query = update.callback_query
    if not query:
        return

    await query.answer()
    data = query.data

    messages = {
        CALLBACK_PROGRAM: 'Скоро покажу программу и текущий доклад.',
        CALLBACK_QUESTION: 'Здесь появится форма для вопроса текущему спикеру.',
        CALLBACK_NETWORKING: 'Подготовим анкету для знакомства и предложим собеседника.',
        CALLBACK_DONATE: 'Добавим кнопку доната и покажем, как поддержать митап.',
        CALLBACK_SUBSCRIBE: 'Настроим подписку на обновления и будущие события.',
    }
    text = messages.get(data, 'Команда в разработке.')

    await query.edit_message_text(text, reply_markup=_menu_keyboard())


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    logger.debug('Unknown command: %s', update.message.text if update.message else 'n/a')
    if update.message:
        await update.message.reply_text('Не понял команду. Используйте /start.')
