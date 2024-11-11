from django.core.exceptions import ValidationError
from django.db.models import (
    BigIntegerField,
    BooleanField,
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    ImageField,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError(_("The image size must be at least 5MB."))


class Messages(AbstractBaseModel):
    user = ForeignKey(
        "BotUsers",
        on_delete=CASCADE,
        verbose_name=_("Foydalanuvchi"),
    )
    chat_id = BigIntegerField(verbose_name=_("Chat ID"))
    message_id = BigIntegerField(verbose_name=_("Message ID"))
    text = TextField(
        null=True,
        blank=True,
        verbose_name=_("Xabar"),
    )
    photo = ImageField(
        upload_to="messages",
        null=True,
        blank=True,
        verbose_name=_("Rasm"),
        validators=[validate_image_size],
    )
    is_answered = BooleanField(default=False, verbose_name=_("Javob berildimi"))

    class Meta:
        db_table = "messages"
        verbose_name = _("Xabar")
        verbose_name_plural = _("Xabarlar")


class Answer(AbstractBaseModel):
    message = ForeignKey(Messages, on_delete=CASCADE, verbose_name=_("Xabar"))
    text = CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Javob"),
    )
    image = ImageField(
        upload_to="answers",
        null=True,
        blank=True,
        verbose_name=_("Rasm"),
        validators=[validate_image_size],
    )

    def __str__(self) -> str:
        return f"{self.created_at} - {self.text}"

    class Meta:
        db_table = "answers"
        verbose_name = _("Javob")
        verbose_name_plural = _("Javoblar")
