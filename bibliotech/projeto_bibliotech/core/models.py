from django.db import models
from django.conf import settings 
from datetime import date

class Categoria(models.Model):
    nome = models.CharField(max_length=100) 

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editora = models.CharField(max_length=100)
    categorias = models.ManyToManyField(Categoria, blank=True)
    capa = models.ImageField(upload_to='capas_livros/', default='capas_livros/default.png')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    data_limite_dias = models.IntegerField(default=15)


    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.titulo


    @property
    def is_available(self):
        return self.quantidade > 0


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('devolvido', 'Devolvido'),
        ('atrasado', 'Atrasado'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    data_devolucao_efetiva = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.username}"


    def save(self, *args, **kwargs):

        is_new = self._state.adding


        if is_new:
            if self.livro.quantidade > 0:
                self.livro.quantidade -= 1
                self.livro.save()
            else:

                raise ValueError("Não é possível reservar um livro sem estoque.")


        if self.status == 'devolvido' and not self.data_devolucao_efetiva:
            self.data_devolucao_efetiva = date.today()

            self.livro.quantidade += 1
            self.livro.save()

        super().save(*args, **kwargs)