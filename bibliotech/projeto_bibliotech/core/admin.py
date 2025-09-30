from django.contrib import admin
from .models import Categoria, Livro, Reserva


class LivroAdmin(admin.ModelAdmin):
    filter_horizontal = ('categorias',)
  
    list_display = ('titulo', 'autor', 'quantidade')


admin.site.register(Categoria)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Reserva)