from modeltranslation.translator import TranslationOptions, register

from apps.rtm.models import Region


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)
