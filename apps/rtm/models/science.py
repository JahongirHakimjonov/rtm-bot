from django.db.models import (
    BooleanField,
    CharField,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Science(AbstractBaseModel):
    name = CharField(max_length=255, verbose_name=_("Fan nomi"))
    is_active = BooleanField(default=True, verbose_name=_("Faolmi"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "sciences"
        verbose_name = _("Fan")
        verbose_name_plural = _("Fanlar")
