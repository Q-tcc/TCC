from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, FotoPerfilForm
from django.contrib.auth.forms import AuthenticationForm
from core.models import Reserva 
from django.contrib import messages
from .models import UsuarioCustomizado

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def ver_perfil_usuario_view(request, usuario_id):
    usuario_alvo = get_object_or_404(UsuarioCustomizado, id=usuario_id)
    
    try:

        livros_reservados_count = Reserva.objects.filter(usuario=usuario_alvo).exclude(status='devolvido').count()
    except Exception:
        livros_reservados_count = 0
    context = {
        'usuario': usuario_alvo, 
        'livros_reservados_count': livros_reservados_count,
    }
    return render(request, 'usuarios/perfil.html', context)

def tela_inicial(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'usuarios/tela_inicial.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tela_inicial')


@login_required
def perfil_view(request):
    foto_form = FotoPerfilForm(instance=request.user)

    if request.method == 'POST':
        foto_form = FotoPerfilForm(request.POST, request.FILES, instance=request.user)
        if foto_form.is_valid():
            foto_form.save()
            messages.success(request, 'Foto de perfil atualizada com sucesso!')
            return redirect('perfil') 
        else:
            messages.error(request, 'Erro ao atualizar a foto.')


    try:
        livros_reservados_count = Reserva.objects.filter(usuario=request.user).exclude(status='devolvido').count() 
    except Exception:
        livros_reservados_count = 0

    context = {
        'usuario': request.user,
        'livros_reservados_count': livros_reservados_count,
        'foto_form': foto_form,
    }
    return render(request, 'usuarios/perfil.html', context)