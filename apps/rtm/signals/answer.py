import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from telebot import TeleBot

from apps.rtm.models import Answer

bot = TeleBot(os.getenv("BOT_TOKEN"))
MAX_PHOTO_SIZE = 10 * 1024 * 1024  # 10 MB


@receiver(post_save, sender=Answer)
def post_save_answer(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.image:  # Assuming `Answer` model has an `image` field
                if os.path.getsize(instance.image.path) > MAX_PHOTO_SIZE:
                    with open(instance.image.path, "rb") as image_file:
                        bot.send_document(
                            instance.message.chat_id,
                            image_file,
                            caption=instance.text,
                            reply_to_message_id=instance.message.message_id,
                        )
                else:
                    with open(instance.image.path, "rb") as image_file:
                        bot.send_photo(
                            instance.message.chat_id,
                            image_file,
                            caption=instance.text,
                            reply_to_message_id=instance.message.message_id,
                        )
            else:
                bot.send_message(
                    instance.message.chat_id,
                    f"{instance.text}",
                    reply_to_message_id=instance.message.message_id,
                )
        except Exception as e:
            print(f"Error sending message: {e}")
        instance.message.is_answered = True
        instance.message.save()
        print(f"New answer created: {instance.text}")
