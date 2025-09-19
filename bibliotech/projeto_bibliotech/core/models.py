from django.db import models
from django.conf import settings 

class Categoria(models.Model):
    nome = models.CharField(max_length=100) 

    def __str__(self):
        return self.nome

class Livro(models.Model):

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editora = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    capa = models.ImageField(upload_to='capas_livros/', default='capas_livros/default.png')
    

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    data_limite_dias = models.IntegerField(default=15) 
    disponivel = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo

class Reserva(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_emprestimo = models.DateField()
    data_devolucao = models.DateField()
    status = models.CharField(max_length=20, default='ativa') 

    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.username}"