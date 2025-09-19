from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro

        fields = ['titulo', 'autor', 'editora', 'categoria', 'capa', 'rating', 'data_limite_dias', 'disponivel']
        

        labels = {
            'titulo': 'Nome',
            'categoria': 'Gênero',
        }