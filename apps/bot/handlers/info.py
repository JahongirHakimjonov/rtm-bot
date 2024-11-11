from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import Message

from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.rtm.models import BotUsers


def handle_info(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    info = BotUsers.objects.get(telegram_id=message.from_user.id)
    text = _(
        f"*ID*: {(str(info.id))}\n"
        f"*Telegram ID*: {(str(info.telegram_id))}\n"
        f"*Username*: {(info.username or '')}\n"
        f"*First name*: {(info.first_name or '')}\n"
        f"*Last name*: {(info.last_name or '')}\n"
        f"*Fullname*: {(info.full_name or '')}\n"
        f"*Phone*: {(info.phone or '')}\n"
        f"*Region*: {(info.region or '')}\n"
        f"*Science*: {(info.science or '')}\n"
        f"*Created at*: {(str(info.created_at))}\n"
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
    )
    logger.info(f"User {message.from_user.id} requested info.")
