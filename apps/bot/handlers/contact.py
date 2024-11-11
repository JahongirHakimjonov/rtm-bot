import requests
from django.core.files.base import ContentFile
from django.utils.translation import activate, gettext as _
from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery

from apps.bot.keyboard import get_main_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.rtm.models import BotUsers
from apps.rtm.models import Messages

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB
8


def handle_contact(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    logger.info(f"User {message.from_user.id} requested contact.")
    contact_button = types.InlineKeyboardButton(
        text=_("Contact"), callback_data="contact"
    )
    cancel_button = types.InlineKeyboardButton(text=_("Cancel"), callback_data="cancel")
    keyboard.add(contact_button, cancel_button)
    bot.send_message(message.chat.id, _("Contact us or cancel:"), reply_markup=keyboard)


def handle_delete_contact_callback(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.message.from_user.id))
    bot.send_message(
        call.message.chat.id, _("Has been canceled."), reply_markup=get_main_buttons()
    )
    bot.delete_message(call.message.chat.id, call.message.message_id)


def handle_contact_callback_query(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.message.from_user.id))
    bot.send_message(
        call.message.chat.id,
        _("Please send your message:"),
        reply_markup=types.ForceReply(selective=True),
    )
    bot.register_next_step_handler(call.message, save_user_message, bot)
    bot.delete_message(call.message.chat.id, call.message.message_id)


def save_user_message(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    user_message = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id
    user = BotUsers.objects.get(telegram_id=user_id)

    # Save the message to Messages model
    sending_message, created = Messages.objects.update_or_create(
        user=user,
        chat_id=chat_id,
        message_id=message_id,
        defaults={"text": user_message},
    )

    # Save the photo if it exists
    if message.photo:
        photo_file_id = message.photo[-1].file_id  # Get the highest resolution photo
        photo_file = bot.get_file(photo_file_id)
        photo_path = photo_file.file_path
        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{photo_path}"

        # Download the photo
        response = requests.get(photo_url)
        if response.status_code == 200:
            if len(response.content) > MAX_PHOTO_SIZE:
                bot.send_message(
                    message.chat.id,
                    _(
                        "The image size must be less than 5MB. Please resend a smaller image."
                    ),
                    reply_to_message_id=message_id,
                )
                bot.register_next_step_handler(message, save_user_message, bot)
                return
            sending_message.photo.save(
                f"{photo_file_id}.jpg", ContentFile(response.content), save=True
            )

    if message.caption:
        sending_message.text = message.caption
        sending_message.save()

    bot.send_message(
        message.chat.id,
        _("Your message has been sent and saved."),
        reply_to_message_id=message_id,
        reply_markup=get_main_buttons(),
    )
