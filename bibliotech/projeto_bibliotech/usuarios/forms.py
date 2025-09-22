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

class PerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioCustomizado
        fields = ['first_name', 'last_name', 'telefone', 'foto_perfil']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'telefone': 'Telefone',
            'foto_perfil': 'Foto de Perfil',
        }
        widgets = {
            'foto_perfil': forms.FileInput(),
        }
