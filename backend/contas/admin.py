from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    ordering = ("email",)
    list_display = ("email", "tipo", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {
            "fields": ("first_name", "last_name", "tipo")
        }),
        ("Permissões", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "tipo",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )