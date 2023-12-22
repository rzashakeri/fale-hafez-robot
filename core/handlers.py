from logging import getLogger

from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from commands.start import start
from commands.take_horoscope import take_horoscope
from constants.keys import GET_OMEN
from constants.states import HOME_STATE

# Init logger

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start, block=False)],
        states={
            HOME_STATE: [
                MessageHandler(
                    filters.Regex(f"^{GET_OMEN}$"),
                    take_horoscope,
                    block=False,
                ),
            ]
        },
        fallbacks=[],
        name="base_conversation_handler",
        persistent=True,
    )
    return conversation_handler
