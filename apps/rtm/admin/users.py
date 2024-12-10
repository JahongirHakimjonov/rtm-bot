from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserCreationForm, UserChangeForm

from apps.rtm.models import BotUsers, LanguageChoices, RoleChoices
from apps.rtm.models import User


@admin.register(BotUsers)
class BotUsersAdmin(ModelAdmin):
    list_display = (
        "id",
        "telegram_id_with_color",
        "language_code_with_color",
        "role_with_color",
        "region_with_color",
        "science_with_color",
        "full_name",
        "phone",
        "username",
        "created_at",
    )
    search_fields = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "phone",
        "full_name",
    )
    list_filter = ("created_at", "updated_at", "is_active", "role", "language_code")
    list_filter_submit = True
    list_display_links = ("id", "telegram_id_with_color")

    @display(
        description=_("Til"),
        label={
            LanguageChoices.UZ: "info",
            LanguageChoices.RU: "info",
        },
    )
    def language_code_with_color(self, obj):
        return obj.language_code, obj.get_language_code_display()

    @display(
        description=_("Rol"),
        label={
            RoleChoices.USER: "warning",
            RoleChoices.MODERATOR: "info",
            RoleChoices.ADMIN: "success",
        },
    )
    def role_with_color(self, obj):
        return obj.role, obj.get_role_display()

    @display(description=_("Telegram ID"), label=True)
    def telegram_id_with_color(self, obj):
        return obj.telegram_id

    @display(description=_("Region"), label=True)
    def region_with_color(self, obj):
        return obj.region.name if obj.region else _("No region")

    @display(description=_("Science"), label=True)
    def science_with_color(self, obj):
        return obj.science.name if obj.science else _("No science")


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ("id", "phone", "username", "is_active", "science")
    search_fields = ("email", "username")
    list_filter = ("is_active", "science")
    list_editable = ("is_active",)
    list_display_links = ("username", "phone", "id")
    fieldsets = (
        (None, {"fields": ("phone", "password", "science")}),
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2", "science", "groups", "is_active", "is_staff"),
            },
        ),
    )
