from django import forms 
from .models import Livro, Reserva

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro

        fields = ['titulo', 'autor', 'editora', 'categorias', 'capa', 'quantidade', 'localizacao']


        widgets = {
            'categorias': forms.CheckboxSelectMultiple,
        }


        labels = {
            'titulo': 'Nome',
            'categorias': 'Gêneros',
            'capa': 'Imagem da Capa',
            'localizacao': 'Localização (Corredor/Prateleira)',
        }
class ReservaAdminForm(forms.ModelForm):

    data_emprestimo = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Data de Empréstimo'
    )
    

    data_devolucao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False, 
        label='Data de Devolução (Prevista)'
    )

    class Meta:
        model = Reserva

        fields = ['data_emprestimo', 'data_devolucao', 'status', 'observacoes']
        
        labels = {
            'status': 'Status da Reserva',
            'observacoes': 'Observações',
        }