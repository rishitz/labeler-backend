from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from authorization.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
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
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login",)},
        ),  # Fix here: tuple instead of string
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    list_display = [
        "uuid",
        "email",
        "first_name",
        "last_name",
        "last_login",
    ]
    search_fields = [
        "email",
        "first_name",
        "last_name",
        "uuid",
    ]


admin.site.unregister(Group)
