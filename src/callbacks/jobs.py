from telegram.ext import ContextTypes
from ..logger import logger
from .waifu import _waifu_graph
import asyncio


async def refresh_data(context: ContextTypes.DEFAULT_TYPE):
    today_waifu: dict = context.bot_data["today_waifu"]

    try:
        await asyncio.gather(
            *(_waifu_graph(chat_id, context) for chat_id in today_waifu.keys())
        )
    except Exception as err:
        logger.error(
            f"{err.__class__.__name__}: {err} happend when performing waifu graph tasks"
        )
        raise err
    finally:
        context.bot_data["today_waifu"] = {}
        context.bot_data["waifu_mutex"] = {}
        context.bot_data["user_info"] = {}
        await context.application.persistence.flush()
        logger.debug("数据已刷新: today_waifu")


async def del_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_message(
        chat_id=context.job.chat_id,
        message_id=context.job.data["message_id"],
    )
