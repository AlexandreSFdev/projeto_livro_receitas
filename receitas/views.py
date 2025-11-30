from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Avg, Q, Count
from django.http import JsonResponse
from .models import Receita, Ingrediente, IngredienteReceita, Avaliacao, Categoria, Comentario
from .forms import ReceitaForm, IngredienteReceitaFormSet

def lista_receitas(request):
    receitas = Receita.objects.all().annotate(media_avaliacoes=Avg('avaliacao__nota'))
    
    # Busca por texto
    busca = request.GET.get('busca', '')
    if busca:
        receitas = receitas.filter(
            Q(titulo__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(modo_preparo__icontains=busca)
        )
    
    # Filtro por dificuldade
    dificuldade = request.GET.get('dificuldade', '')
    if dificuldade:
        receitas = receitas.filter(dificuldade=dificuldade)
    
    # Filtro por tempo máximo
    tempo_max = request.GET.get('tempo_max', '')
    if tempo_max:
        receitas = receitas.filter(tempo_preparo__lte=tempo_max)
    
    # Ordenação
    ordenar = request.GET.get('ordenar', '-criado_em')
    if ordenar == 'mais_recentes':
        receitas = receitas.order_by('-criado_em')
    elif ordenar == 'mais_antigas':
        receitas = receitas.order_by('criado_em')
    elif ordenar == 'tempo_crescente':
        receitas = receitas.order_by('tempo_preparo')
    elif ordenar == 'tempo_decrescente':
        receitas = receitas.order_by('-tempo_preparo')
    elif ordenar == 'melhor_avaliadas':
        receitas = receitas.order_by('-media_avaliacoes')
    
    context = {
        'receitas': receitas,
        'busca': busca,
        'dificuldade': dificuldade,
        'tempo_max': tempo_max,
        'ordenar': ordenar,
    }
    
    return render(request, 'receitas/lista.html', context)


def detalhe_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    
    # Incrementar visualizações
    receita.visualizacoes += 1
    receita.save(update_fields=['visualizacoes'])
    
    ingredientes = receita.ingredientereceita_set.all()
    info_nutricional = receita.calcular_informacoes_nutricionais()
    avaliacoes = receita.avaliacao_set.all().order_by('-criado_em')
    media_avaliacoes = avaliacoes.aggregate(Avg('nota'))['nota__avg']
    comentarios = receita.comentarios.all()
    
    # Verificar se está favoritado
    esta_favoritado = False
    if request.user.is_authenticated:
        esta_favoritado = request.user in receita.favoritos.all()
    
    # Processar avaliação
    if request.method == 'POST' and request.user.is_authenticated:
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario', '')
        
        if nota:
            avaliacao, created = Avaliacao.objects.update_or_create(
                receita=receita,
                usuario=request.user,
                defaults={'nota': nota, 'comentario': comentario}
            )
            messages.success(request, 'Avaliação salva com sucesso!')
            return redirect('detalhe_receita', pk=pk)
    
    context = {
        'receita': receita,
        'ingredientes': ingredientes,
        'info_nutricional': info_nutricional,
        'avaliacoes': avaliacoes,
        'media_avaliacoes': media_avaliacoes,
        'comentarios': comentarios,
        'esta_favoritado': esta_favoritado,
    }
    return render(request, 'receitas/detalhe.html', context)


@login_required
def criar_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        formset = IngredienteReceitaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)
            receita.autor = request.user
            receita.save()
            
            # Salvar categorias (ManyToMany precisa salvar depois do objeto)
            form.save_m2m()
            
            # Salvar ingredientes
            formset.instance = receita
            formset.save()
            
            messages.success(request, 'Receita criada com sucesso!')
            return redirect('detalhe_receita', pk=receita.pk)
        else:
            # Mostrar erros
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            if formset.errors:
                messages.error(request, 'Verifique os ingredientes. É necessário pelo menos 1 ingrediente.')
    else:
        form = ReceitaForm()
        formset = IngredienteReceitaFormSet()
    
    return render(request, 'receitas/form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Nova Receita'
    })


@login_required
def editar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES, instance=receita)
        formset = IngredienteReceitaFormSet(request.POST, instance=receita)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Receita atualizada com sucesso!')
            return redirect('detalhe_receita', pk=receita.pk)
    else:
        form = ReceitaForm(instance=receita)
        formset = IngredienteReceitaFormSet(instance=receita)
    
    return render(request, 'receitas/form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Editar Receita'
    })


@login_required
def deletar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk, autor=request.user)
    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita deletada com sucesso!')
        return redirect('lista_receitas')
    return render(request, 'receitas/confirmar_delete.html', {'receita': receita})


@login_required
def minhas_receitas(request):
    receitas = Receita.objects.filter(autor=request.user).annotate(
        media_avaliacoes=Avg('avaliacao__nota')
    )
    return render(request, 'receitas/minhas_receitas.html', {'receitas': receitas})


# Favoritos
@login_required
def toggle_favorito(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    
    if request.user in receita.favoritos.all():
        receita.favoritos.remove(request.user)
        favoritado = False
        messages.info(request, 'Receita removida dos favoritos.')
    else:
        receita.favoritos.add(request.user)
        favoritado = True
        messages.success(request, 'Receita adicionada aos favoritos!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'favoritado': favoritado,
            'total_favoritos': receita.favoritos.count()
        })
    
    return redirect('detalhe_receita', pk=pk)


@login_required
def receitas_favoritas(request):
    receitas = request.user.receitas_favoritas.all().annotate(
        media_avaliacoes=Avg('avaliacao__nota')
    )
    return render(request, 'receitas/favoritas.html', {'receitas': receitas})


# Categorias
def receitas_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    receitas = categoria.receitas.all().annotate(
        media_avaliacoes=Avg('avaliacao__nota')
    )
    return render(request, 'receitas/por_categoria.html', {
        'categoria': categoria,
        'receitas': receitas
    })


def todas_categorias(request):
    categorias = Categoria.objects.annotate(
        total_receitas=Count('receitas')
    )
    return render(request, 'receitas/categorias.html', {'categorias': categorias})


# Comentários
@login_required
def adicionar_comentario(request, pk):
    if request.method == 'POST':
        receita = get_object_or_404(Receita, pk=pk)
        texto = request.POST.get('texto')
        
        if texto:
            Comentario.objects.create(
                receita=receita,
                usuario=request.user,
                texto=texto
            )
            messages.success(request, 'Comentário adicionado!')
    
    return redirect('detalhe_receita', pk=pk)


# Receitas Populares
def receitas_populares(request):
    receitas = Receita.objects.all().annotate(
        media_avaliacoes=Avg('avaliacao__nota')
    ).order_by('-visualizacoes')[:20]
    
    return render(request, 'receitas/populares.html', {'receitas': receitas})


# Autenticação
def login_view(request):
    if request.user.is_authenticated:
        return redirect('lista_receitas')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'lista_receitas')
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'receitas/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('lista_receitas')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('lista_receitas')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('lista_receitas')
    else:
        form = UserCreationForm()
    
    return render(request, 'receitas/registro.html', {'form': form})
