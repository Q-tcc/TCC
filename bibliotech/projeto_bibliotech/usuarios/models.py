from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioCustomizado(AbstractUser):
    
    escolha_genero = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar'),
    ]


    telefone = models.CharField(max_length=15, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default_profile.png')


    genero = models.CharField(max_length=1, choices=escolha_genero, blank=True, null=True)

    def __str__(self):
        return self.username