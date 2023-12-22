import time
from random import randint
import openpyxl
from logging import getLogger
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from constants.messages import POETRY, DESCRIPTION
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


def select_random_horoscope() -> any:
    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook('fale_hafez.xlsx')
    sheet = workbook.active

    # Determine the size of the sheet
    max_row = sheet.max_row

    # Generate a random row and column index
    random_row = randint(1, max_row) - 1

    # Get the random cell
    random_fal = sheet[random_row]

    # Don't forget to close the workbook if you're done with it
    workbook.close()

    cleaned_text = {
        'poetry': random_fal[1].value.replace('_x000D_', ''),
        'description': random_fal[2].value.replace('_x000D_', '')
    }

    return cleaned_text


@send_action(ChatAction.TYPING)
async def take_horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument

    number_three = await context.bot.send_message(
        chat_id=update.message.chat_id, text="3️⃣"
    )
    time.sleep(1)
    await context.bot.deleteMessage(
        message_id=number_three.message_id,
        chat_id=update.message.chat_id
    )

    number_two = await context.bot.send_message(
        chat_id=update.message.chat_id, text="2️⃣"
    )
    time.sleep(1)
    await context.bot.deleteMessage(
        message_id=number_two.message_id,
        chat_id=update.message.chat_id
    )

    number_one = await context.bot.send_message(
        chat_id=update.message.chat_id, text="1️⃣"
    )
    time.sleep(1)
    await context.bot.deleteMessage(
        message_id=number_one.message_id,
        chat_id=update.message.chat_id
    )
    horoscope = select_random_horoscope()
    poetry = horoscope.get("poetry")
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=POETRY.format(poetry=poetry)
    )

    description = horoscope.get("description")

    # Split the text by spaces to simulate typing
    description_words = description.split()

    # Send a message that will be edited later
    message = await context.bot.send_message(chat_id=update.message.chat_id, text="معنی فال شما 👇 \n")

    displayed_text = "معنی فال شما 👇 \n\n"
    for word in description_words:
        displayed_text += f"{word} "

        # send chat action (is typing ...)
        await context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id,
            action=ChatAction.TYPING
        )

        # Edit the message with the new text
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=message.message_id,
            text=displayed_text
        )

    await context.bot.edit_message_text(
        chat_id=update.message.chat_id,
        message_id=message.message_id,
        text=DESCRIPTION.format(description=description)
    )
