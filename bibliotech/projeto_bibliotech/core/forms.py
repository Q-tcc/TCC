from django import forms 
from .models import Livro, Reserva

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro

        fields = ['titulo', 'autor', 'editora', 'categorias', 'capa', 'quantidade']


        widgets = {
            'categorias': forms.CheckboxSelectMultiple,
        }


        labels = {
            'titulo': 'Nome',
            'categorias': 'Gêneros',
            'capa': 'Imagem da Capa',
        }
class ReservaAdminForm(forms.ModelForm):
    data_devolucao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Reserva
        fields = ['data_devolucao', 'status', 'observacoes']
        labels = {
            'data_devolucao': 'Adiar data de devolução para',
            'status': 'Status da Reserva (marcar como "Devolvido")',
            'observacoes': 'Observações (após devolução)',
        }
