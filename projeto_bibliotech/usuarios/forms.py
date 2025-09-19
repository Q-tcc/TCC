from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioCustomizado

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioCustomizado
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UsuarioCustomizado
        fields = ('first_name', 'last_name', 'email', 'telefone', 'foto_perfil')