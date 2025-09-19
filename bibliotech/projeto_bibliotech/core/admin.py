from django.contrib import admin
from .models import Categoria, Livro, Reserva


admin.site.register(Categoria)
admin.site.register(Livro)
admin.site.register(Reserva)