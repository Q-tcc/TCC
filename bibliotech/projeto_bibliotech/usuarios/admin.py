from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import UsuarioCustomizado

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    model = UsuarioCustomizado

    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telefone', 'foto_perfil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('telefone',)}),
    )


admin.site.register(UsuarioCustomizado, CustomUserAdmin)