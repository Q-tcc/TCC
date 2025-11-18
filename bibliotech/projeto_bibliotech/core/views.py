from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Livro, Categoria, Reserva
from .forms import LivroForm, ReservaAdminForm
from datetime import date, timedelta
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from django.http import JsonResponse

def adicionar_dias_uteis(data_inicial, dias):
    data_final = data_inicial
    while dias > 0:
        data_final += timedelta(days=1)
        if data_final.weekday() < 5:
            dias -= 1
    return data_final

def is_admin(user):
    return user.is_staff


@login_required
def home_view(request):
    
    if request.user.is_staff:

        return render(request, 'core/home_adm.html')
    else:

        return render(request, 'core/home_cliente.html')

def home_convidado_view(request):

    return render(request, 'core/home_convidado.html')


def catalogo_view(request):

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
    
    reserva_do_usuario = None


    if request.user.is_authenticated:

        reserva_do_usuario = Reserva.objects.filter(
            livro=livro, 
            usuario=request.user, 

            status__in=['ativa', 'atrasado', 'preparando', 'aguardando_retirada']
        ).first()

    context = {
        'livro': livro,
        'livros_similares': livros_similares,
        'reserva_do_usuario': reserva_do_usuario, 
    }
    return render(request, 'core/livro_detalhe.html', context)


@login_required
def reservar_livro_view(request, livro_id):
    if request.user.is_staff:
        messages.error(request, 'Administradores não podem reservar livros.')
        return redirect('livro_detalhe', livro_id=livro_id)
        
    livro = get_object_or_404(Livro, id=livro_id)
    
    ja_reservado = Reserva.objects.filter(
        livro=livro, 
        usuario=request.user
    ).exclude(status='devolvido').exists()
    

    total_emprestimos = Reserva.objects.filter(usuario=request.user).exclude(status='devolvido').count()
    if total_emprestimos >= 3:
        messages.error(request, 'Você atingiu o limite máximo de 3 livros reservados.')
        return redirect('livro_detalhe', livro_id=livro_id)
    
    if request.method == 'POST':

        if ja_reservado:
             messages.warning(request, 'Você já possui uma reserva ativa deste livro.')
             return redirect('livro_detalhe', livro_id=livro_id)


        if livro.is_available:
            data_pronto = adicionar_dias_uteis(date.today(), 2)
            
            Reserva.objects.create(
                livro=livro,
                usuario=request.user,
                data_disponivel=data_pronto,
                status='preparando',
                data_devolucao=None
            )

            
            messages.success(request, 'Livro reservado com sucesso! Aguarde a preparação.')
            return redirect('reservas_cliente')
        

        else:
            messages.error(request, 'Livro indisponível (Sem estoque).')
            return redirect('livro_detalhe', livro_id=livro_id)
    
    return redirect('livro_detalhe', livro_id=livro_id)

@login_required
def reservas_cliente_view(request):

    reservas = Reserva.objects.filter(usuario=request.user).exclude(status='devolvido').order_by('-data_reserva')
    return render(request, 'core/reservas_cliente.html', {'reservas': reservas})

@user_passes_test(is_admin)
def reservas_adm_view(request):

    reservas = Reserva.objects.annotate(

        ordem_prioridade=Case(
            When(status='devolvido', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('ordem_prioridade', '-id') 

    return render(request, 'core/reservas_adm.html', {'reservas': reservas})

@user_passes_test(is_admin)
def editar_reserva_adm_view(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaAdminForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva atualizada com sucesso!')
            return redirect('reservas_adm')
    else:
        form = ReservaAdminForm(instance=reserva)

    context = {
        'form': form,
        'reserva': reserva,
        'titulo_pagina': f"Editar Reserva de '{reserva.livro.titulo}'"
    }
    return render(request, 'core/editar_reserva_adm.html', context)


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

        form = LivroForm(request.POST, request.FILES, instance=livro)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('livro_detalhe', livro_id=livro.id)
        else:

            print(form.errors)
    else:

        form = LivroForm(instance=livro)
        
    return render(request, 'core/livro_form.html', {
        'form': form, 
        'titulo_pagina': 'Editar Livro'
    })

@user_passes_test(is_admin)
def excluir_livro_view(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)


    if request.method == 'POST':
        titulo_livro = livro.titulo 
        livro.delete()
        messages.success(request, f"O livro '{titulo_livro}' foi excluído com sucesso.")
        return redirect('catalogo')


    return render(request, 'core/livro_confirm_delete.html', {'livro': livro})


def creditos_view(request):
    return render(request, 'core/creditos.html')

def buscar_livros_api(request):
    query = request.GET.get('q', '')
    if query:
        
        livros = Livro.objects.filter(titulo__icontains=query)[:5]
        results = []
        for livro in livros:
            results.append({
                'id': livro.id,
                'titulo': livro.titulo,
                'autor': livro.autor,
                'capa_url': livro.capa.url if livro.capa else ''
            })
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})