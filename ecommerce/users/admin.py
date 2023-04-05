from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ecommerce.users.forms import UserAdminChangeForm, UserAdminCreationForm
from ecommerce.users.models import UserProfile
from ecommerce.utils.admin import CustomAdminFileWidget

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    can_delete = False
    fieldsets = (
        (
            _("Personal Info"),
            {
                "fields": (
                    "full_name",
                    "birth_date",
                    "country",
                    "language",
                )
            },
        ),
        (_("Avatar"), {"fields": ("avatar",)}),
        (_("Contact Options"), {"fields": ("website", "phone", "contact_email")}),
    )
    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}
    classes = ("grp-collapse grp-open",)
    inline_classes = ("grp-collapse grp-open",)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password", "email")}),
        (_("Profile"), {"classes": ("placeholder profile-group",), "fields": ()}),
        (
            _("Permissions"),
            {
                "classes": ("grp-collapse grp-closed",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "is_superuser"]
    search_fields = ["username"]
    readonly_fields = ["last_login", "date_joined"]
    inlines = (UserProfileInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ["username"]
        return self.readonly_fields
