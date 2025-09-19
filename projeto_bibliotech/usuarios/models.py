from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioCustomizado(AbstractUser):
    
    telefone = models.CharField(max_length=15, blank=True, null=True)
    
   
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True, default='fotos_perfil/default.png') 

    

    def __str__(self):
        return self.username