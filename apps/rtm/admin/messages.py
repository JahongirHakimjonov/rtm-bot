from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.rtm.models import Messages, Answer


class AnswerInline(TabularInline):
    model = Answer
    extra = 1


@admin.register(Messages)
class MessagesAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "text",
        "is_answered",
        "created_at",
    )
    search_fields = (
        "user",
        "user__telegram_id",
        "chat_id",
        "message_id",
        "text",
    )
    list_filter = ("created_at", "updated_at", "is_answered")
    list_filter_submit = True
    list_display_links = ("id", "user", "chat_id", "message_id")
    inlines = (AnswerInline,)
    readonly_fields = ("user", "text", "is_answered")
    exclude = ("chat_id", "message_id")


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = (
        "id",
        "message",
        "text",
        "created_at",
    )
    search_fields = (
        "message",
        "text",
    )
    list_filter = ("created_at", "updated_at")
    list_filter_submit = True
    list_display_links = ("id", "message", "text")
