from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioCustomizado
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioCustomizado
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'telefone', 'genero')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].max_length = 20
        self.fields['username'].widget.attrs['maxlength'] = '20'

        self.fields['first_name'].max_length = 20
        self.fields['first_name'].widget.attrs['maxlength'] = '20'

        self.fields['last_name'].max_length = 20
        self.fields['last_name'].widget.attrs['maxlength'] = '20'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("O usuário deve conter apenas letras e números (sem espaços ou símbolos).")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            if not re.match(r'^[a-zA-Z0-9 ]+$', first_name):
                raise forms.ValidationError("O nome não pode conter caracteres especiais (@, !, #, etc).")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            if not re.match(r'^[a-zA-Z0-9 ]+$', last_name):
                raise forms.ValidationError("O sobrenome não pode conter caracteres especiais.")
        return last_name

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            return re.sub(r'\D', '', telefone)
        return telefone
        
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