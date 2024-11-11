import re

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

    # Escape special characters for MarkdownV2
    def escape_markdown(text):
        return re.sub(r'([*_`\[\]()~>#+-=|{}.!])', r'\\\1', text or '')

    text = _(
        f"*ID*: {escape_markdown(str(info.id))}\n"
        f"*Telegram ID*: {escape_markdown(str(info.telegram_id))}\n"
        f"*Username*: {escape_markdown(info.username)}\n"
        f"*First name*: {escape_markdown(info.first_name)}\n"
        f"*Last name*: {escape_markdown(info.last_name)}\n"
        f"*Fullname*: {escape_markdown(info.full_name)}\n"
        f"*Phone*: {escape_markdown(info.phone)}\n"
        f"*Region*: {escape_markdown(info.region)}\n"
        f"*Science*: {escape_markdown(info.science)}\n"
        f"*Created at*: {escape_markdown(str(info.created_at))}\n"
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
    )
    logger.info(f"User {message.from_user.id} requested info.")
