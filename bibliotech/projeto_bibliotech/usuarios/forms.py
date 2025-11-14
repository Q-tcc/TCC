from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioCustomizado
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioCustomizado
        fields = ('username', 'first_name', 'last_name', 'email','genero', 'telefone')
        
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            return re.sub(r'\D', '', telefone)
        return telefone


class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioCustomizado
        fields = ['foto_perfil']
        labels = { 'foto_perfil': 'Nova Foto de Perfil' }
        widgets = {
            'foto_perfil': forms.FileInput(attrs={'accept': 'image/*'})
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UsuarioCustomizado
        fields = ('first_name', 'last_name', 'email', 'telefone', 'foto_perfil')