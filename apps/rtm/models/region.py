from django.db.models import (
    BooleanField,
    CharField,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Region(AbstractBaseModel):
    name = CharField(max_length=255, verbose_name=_("Viloyat nomi"))
    is_active = BooleanField(default=True, verbose_name=_("Faolmi"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "regions"
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")
