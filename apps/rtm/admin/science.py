from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.rtm.models import Science


@admin.register(Science)
class RegionAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    list_filter_submit = True
    list_display_links = ("id", "name")
