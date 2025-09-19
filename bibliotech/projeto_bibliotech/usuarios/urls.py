from django.urls import path
from . import views

urlpatterns = [

    
    path('', views.tela_inicial, name='tela_inicial'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
]