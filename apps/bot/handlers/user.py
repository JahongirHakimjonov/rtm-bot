import re

from django.utils.translation import activate, gettext as _
from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from apps.bot.keyboard import get_main_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.rtm.models import BotUsers, Region, Science


def any_user(message: Message, bot: TeleBot):
    try:
        activate(set_language_code(message.from_user.id))
        update_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_active=True,
        )
        logger.info(f"User {message.from_user.id} started the bot.")

        # Step 1: Prompt the user to select their language
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        uz_button = types.InlineKeyboardButton(text="O'zbek", callback_data="lan_uz")
        ru_button = types.InlineKeyboardButton(text="Русский", callback_data="lan_ru")
        keyboard.add(uz_button, ru_button)
        bot.send_message(
            message.chat.id,
            "Tilni tanlang / Выберите язык",
            reply_markup=keyboard,
        )

    except Exception as e:
        bot.send_message(message.chat.id, _("An error occurred."))
        logger.error(f"Error in any_user: {e}")


def handle_full_name(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    full_name = message.text
    user = BotUsers.objects.get(telegram_id=message.from_user.id)
    user.full_name = full_name
    user.save()
    markup = ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True
    )
    phone_button = KeyboardButton(_("Telefon raqamni yuborish"), request_contact=True)
    markup.add(phone_button)
    bot.send_message(
        message.chat.id, _("Please enter your phone number:"), reply_markup=markup
    )
    bot.register_next_step_handler(message, handle_phone, bot)


def handle_phone(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    phone = None
    regex_pattern = r"^\+?998[\d\s\-\(\)]{9}$"

    if message.contact:
        phone = message.contact.phone_number
    elif message.text and re.match(regex_pattern, message.text):
        phone = re.sub(r"[^\d]", "", message.text)
    else:
        bot.send_message(
            message.chat.id,
            _("Yaroqsiz telefon raqam formati. Iltimos, qayta urinib ko'ring."),
        )
        bot.register_next_step_handler(message, handle_phone, bot)
        return

    user = BotUsers.objects.get(telegram_id=message.from_user.id)
    user.phone = phone
    user.save()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    regions = Region.objects.all()
    buttons = [
        types.InlineKeyboardButton(
            text=region.name, callback_data=f"region_{region.id}"
        )
        for region in regions
    ]
    keyboard.add(*buttons)
    bot.send_message(
        message.chat.id, _("Please select your region:"), reply_markup=keyboard
    )


def handle_region_selection(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.from_user.id))
    region_id = int(call.data.split("_")[1])
    user = BotUsers.objects.get(telegram_id=call.from_user.id)
    user.region_id = region_id
    user.save()

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    sciences = Science.objects.all()
    buttons = [
        types.InlineKeyboardButton(
            text=science.name, callback_data=f"science_{science.id}"
        )
        for science in sciences
    ]
    keyboard.add(*buttons)
    bot.send_message(
        call.message.chat.id,
        _("Please select your science field:"),
        reply_markup=keyboard,
    )
    bot.delete_message(call.message.chat.id, call.message.message_id)


def handle_science_selection(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.from_user.id))
    science_id = int(call.data.split("_")[1])
    user = BotUsers.objects.get(telegram_id=call.from_user.id)
    user.science_id = science_id
    user.save()

    bot.send_message(
        call.message.chat.id,
        _("Thank you! Your information has been updated."),
        reply_markup=get_main_buttons(),
    )
    bot.delete_message(call.message.chat.id, call.message.message_id)
    logger.info(f"User {call.from_user.id} completed the registration process.")
