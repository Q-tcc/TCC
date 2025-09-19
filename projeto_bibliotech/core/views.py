from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Livro, Categoria, Reserva
from .forms import LivroForm
from datetime import date, timedelta
from django.contrib import messages


def is_admin(user):
    return user.is_staff


@login_required
def home_view(request):
    
    if request.user.is_staff:
        #adm
        return render(request, 'core/home_adm.html')
    else:
        #cliente
        return render(request, 'core/home_cliente.html')

def home_convidado_view(request):
    #convidado
    return render(request, 'core/home_convidado.html')

#catalogo
def catalogo_view(request):
    #livros por categoria
    categorias = Categoria.objects.all()
    livros_por_categoria = {}
    for categoria in categorias:
        livros = Livro.objects.filter(categorias=categoria)
        livros_por_categoria[categoria.nome] = livros
        
    context = {
        'livros_por_categoria': livros_por_categoria
    }
    return render(request, 'core/catalogo.html', context)

def livro_detalhe_view(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    categorias_do_livro = livro.categorias.all()
    livros_similares = Livro.objects.filter(categorias__in=categorias_do_livro).exclude(id=livro_id).distinct()[:5]

    context = {
        'livro': livro,
        'livros_similares': livros_similares
    }
    return render(request, 'core/livro_detalhe.html', context)

#reserva
@login_required
def reservar_livro_view(request, livro_id):
    if request.user.is_staff:
        messages.error(request, 'Administradores não podem reservar livros.')
        return redirect('livro_detalhe', livro_id=livro_id)
        
    livro = get_object_or_404(Livro, id=livro_id)
    
    ja_reservado = Reserva.objects.filter(livro=livro, usuario=request.user, status='ativa').exists()
    
    if request.method == 'POST':
        if livro.disponivel and not ja_reservado:
            #criar reserva
            data_emprestimo = date.today()
            data_devolucao = data_emprestimo + timedelta(days=livro.data_limite_dias)
            
            Reserva.objects.create(
                livro=livro,
                usuario=request.user,
                data_emprestimo=data_emprestimo,
                data_devolucao=data_devolucao,
                status='ativa'
            )
            

            
            messages.success(request, 'Livro reservado com sucesso!')
            return redirect('reservas_cliente')
        else:
            messages.error(request, 'Livro indisponível ou já reservado por você.')
            return redirect('livro_detalhe', livro_id=livro_id)
    

    return redirect('livro_detalhe', livro_id=livro_id)

@login_required
def reservas_cliente_view(request):
    #minhas reservas
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_emprestimo')
    return render(request, 'core/reservas_cliente.html', {'reservas': reservas})

@user_passes_test(is_admin)
def reservas_adm_view(request):

    reservas = Reserva.objects.all().order_by('-data_emprestimo')
    return render(request, 'core/reservas_adm.html', {'reservas': reservas})

#adm
@user_passes_test(is_admin)
def adicionar_livro_view(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro adicionado com sucesso!') 
            return redirect('catalogo')
        else:

            print("ERROS NO FORMULÁRIO:", form.errors.as_json())
    else:
        form = LivroForm()

    context = {
        'form': form,
        'titulo_pagina': 'Novo Livro'
    }
    return render(request, 'core/livro_form.html', context)

@user_passes_test(is_admin)
def editar_livro_view(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES, instance=Livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('livro_detalhe', livro_id=livro.id)
    else:
        form = LivroForm(instance=livro)
    return render(request, 'core/livro_form.html', {'form': form, 'titulo_pagina': 'Editar Livro', 'livro': livro})

@user_passes_test(is_admin)
def excluir_livro_view(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if request.method == 'POST': 
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso.')
        return redirect('catalogo')
 
    return render(request, 'core/livro_confirm_delete.html', {'livro': livro})


def creditos_view(request):
    return render(request, 'core/creditos.html')

#def filtro(request):

