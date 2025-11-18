from django.urls import path
from . import views

urlpatterns = [



    path('home/', views.home_view, name='home'),
    path('home-convidado/', views.home_convidado_view, name='home_convidado'),

    # Catálogo e Livros
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('livro/<int:livro_id>/', views.livro_detalhe_view, name='livro_detalhe'),
    path('api/buscar-livros/', views.buscar_livros_api, name='buscar_livros_api'),
    
    # Reservas
    path('livro/<int:livro_id>/reservar/', views.reservar_livro_view, name='processar_reserva'),
    path('minhas-reservas/', views.reservas_cliente_view, name='reservas_cliente'),
    path('gerenciar-reservas/', views.reservas_adm_view, name='reservas_adm'),

    # CRUD de Livros (Admin)
    path('livro/adicionar/', views.adicionar_livro_view, name='adicionar_livro'),
    path('livro/<int:livro_id>/editar/', views.editar_livro_view, name='editar_livro'),
    path('livro/<int:livro_id>/excluir/', views.excluir_livro_view, name='excluir_livro'),

    path('creditos/', views.creditos_view, name='creditos'),
    path('gerenciar-reservas/', views.reservas_adm_view, name='reservas_adm'),
    path('gerenciar-reservas/<int:reserva_id>/editar/', views.editar_reserva_adm_view, name='editar_reserva_adm'),

]