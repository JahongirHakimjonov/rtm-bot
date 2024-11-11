from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Bosh sahifa"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Foydalanuvchilar"),
        "items": [
            {
                "title": _("Guruhlar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("RTM bot"),
        "items": [
            {
                "title": _("Bot Foydalanuvchilari"),
                "icon": "robot_2",
                "link": reverse_lazy("admin:rtm_botusers_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_botusers"
                ),
            },
            {
                "title": _("Murojaatlar"),
                "icon": "forum",
                "link": reverse_lazy("admin:rtm_messages_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_messages"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("RTM bot qo'shimcha"),
        "items": [
            {
                "title": _("Viloyatlar"),
                "icon": "south_america",
                "link": reverse_lazy("admin:rtm_region_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_region"
                ),
            },
            {
                "title": _("Fanlar"),
                "icon": "menu_book",
                "link": reverse_lazy("admin:rtm_science_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_science"
                ),
            },
        ],
    },
]
