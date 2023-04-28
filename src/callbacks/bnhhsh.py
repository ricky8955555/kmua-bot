from telegram import (
    Update,
)
from telegram.ext import ContextTypes

from ..logger import logger
from ..bnhhsh.bnhhsh import dp
from ..utils import message_recorder

import re


async def bnhhsh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"[{update.effective_chat.title}]({update.effective_user.name})"
        + f" {update.effective_message.text}"
    )
    await message_recorder(update, context)
    text = update.effective_message.text.removeprefix(f"@{context.bot.username}")
    english_words = re.findall(r"[A-Za-z]+", text)
    english_words = list(set(english_words))
    translated_words = [dp(word.lower()) for word in english_words]
    text = ""
    for i in range(len(english_words)):
        text += english_words[i] + ": " + translated_words[i] + "\n"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )
