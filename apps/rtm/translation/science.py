from modeltranslation.translator import TranslationOptions, register

from apps.rtm.models import Science


@register(Science)
class ScienceTranslationOptions(TranslationOptions):
    fields = ("name",)
