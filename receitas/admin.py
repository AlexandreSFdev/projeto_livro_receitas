from django.contrib import admin
from .models import Receita, Ingrediente, IngredienteReceita, Avaliacao, Categoria, Comentario, FotoReceita

class IngredienteReceitaInline(admin.TabularInline):
    model = IngredienteReceita
    extra = 1

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'tempo_preparo', 'dificuldade', 'visualizacoes', 'criado_em']
    list_filter = ['dificuldade', 'criado_em', 'categorias']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['categorias', 'favoritos']
    readonly_fields = ['visualizacoes', 'criado_em', 'atualizado_em']
    inlines = [IngredienteReceitaInline]

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'calorias_por_100g', 'proteinas_por_100g']
    search_fields = ['nome']

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['receita', 'usuario', 'nota', 'criado_em']
    list_filter = ['nota', 'criado_em']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'cor']
    search_fields = ['nome']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'receita', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['usuario__username', 'receita__titulo', 'texto']

@admin.register(FotoReceita)
class FotoReceitaAdmin(admin.ModelAdmin):
    list_display = ['receita', 'legenda', 'criado_em']
    list_filter = ['criado_em']