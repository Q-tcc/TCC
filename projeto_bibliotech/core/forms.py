from django import forms 
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro

        fields = ['titulo', 'autor', 'editora', 'categorias', 'capa', 'disponivel']


        widgets = {
            'categorias': forms.CheckboxSelectMultiple,
        }


        labels = {
            'titulo': 'Nome',
            'categorias': 'Gêneros',
            'capa': 'Imagem da Capa',
        }