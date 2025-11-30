from django.db import models
from django.contrib.auth.models import User
import requests


# 1. DEFINIR CATEGORIA PRIMEIRO (antes de usar em Receita)
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, default='bi-bookmark')
    cor = models.CharField(max_length=20, default='primary')
    
    class Meta:
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.nome


# 2. INGREDIENTE
class Ingrediente(models.Model):
    nome = models.CharField(max_length=200)
    calorias_por_100g = models.FloatField(null=True, blank=True)
    proteinas_por_100g = models.FloatField(null=True, blank=True)
    carboidratos_por_100g = models.FloatField(null=True, blank=True)
    gorduras_por_100g = models.FloatField(null=True, blank=True)
    acucares_por_100g = models.FloatField(null=True, blank=True)
    sodio_por_100g = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Ingredientes"
    
    def __str__(self):
        return self.nome


# 3. RECEITA (agora pode usar Categoria)
class Receita(models.Model):
    DIFICULDADE_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField(help_text="Tempo em minutos")
    porcoes = models.IntegerField(default=1)
    dificuldade = models.CharField(max_length=10, choices=DIFICULDADE_CHOICES)
    foto = models.ImageField(upload_to='receitas/', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    # NOVOS CAMPOS
    categorias = models.ManyToManyField(Categoria, blank=True, related_name='receitas')
    visualizacoes = models.IntegerField(default=0)
    favoritos = models.ManyToManyField(User, blank=True, related_name='receitas_favoritas')
    
    class Meta:
        verbose_name_plural = "Receitas"
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.titulo
    
    def calcular_informacoes_nutricionais(self):
        """Calcula informações nutricionais totais da receita"""
        total = {
            'calorias': 0,
            'proteinas': 0,
            'carboidratos': 0,
            'gorduras': 0,
            'acucares': 0,
            'sodio': 0
        }
        
        for item in self.ingredientereceita_set.all():
            quantidade_em_gramas = item.quantidade
            ingrediente = item.ingrediente
            
            if ingrediente.calorias_por_100g:
                total['calorias'] += (quantidade_em_gramas / 100) * ingrediente.calorias_por_100g
            if ingrediente.proteinas_por_100g:
                total['proteinas'] += (quantidade_em_gramas / 100) * ingrediente.proteinas_por_100g
            if ingrediente.carboidratos_por_100g:
                total['carboidratos'] += (quantidade_em_gramas / 100) * ingrediente.carboidratos_por_100g
            if ingrediente.gorduras_por_100g:
                total['gorduras'] += (quantidade_em_gramas / 100) * ingrediente.gorduras_por_100g
            if ingrediente.acucares_por_100g:
                total['acucares'] += (quantidade_em_gramas / 100) * ingrediente.acucares_por_100g
            if ingrediente.sodio_por_100g:
                total['sodio'] += (quantidade_em_gramas / 100) * ingrediente.sodio_por_100g
        
        return total


# 4. INGREDIENTE RECEITA
class IngredienteReceita(models.Model):
    UNIDADE_CHOICES = [
        ('g', 'Grama(s)'),
        ('kg', 'Quilograma(s)'),
        ('ml', 'Mililitro(s)'),
        ('l', 'Litro(s)'),
        ('un', 'Unidade'),
        ('xic', 'Xícara(s)'),
        ('col_sopa', 'Colher(s) de Sopa'),
        ('col_cha', 'Colher(s) de Chá'),
        ('pitada', 'Pitada(s)'),
        ('fatia', 'Fatia(s)'),
        ('copo', 'Copo(s)'),
        ('pacote', 'Pacote(s)'),
        ('lata', 'Lata(s)'),
        ('outro', 'Outro'),
    ]
    
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.FloatField(help_text="Quantidade em gramas (converter outras unidades)")
    unidade = models.CharField(max_length=10, choices=UNIDADE_CHOICES)
    observacao = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = "Ingrediente da Receita"
        verbose_name_plural = "Ingredientes da Receita"
    
    def __str__(self):
        return f"{self.quantidade}{self.unidade} de {self.ingrediente.nome}"


# 5. AVALIAÇÃO
class Avaliacao(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ['receita', 'usuario']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.receita.titulo} ({self.nota}★)"


# 6. COMENTÁRIO
class Comentario(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.receita.titulo}"


# 7. FOTO EXTRA DA RECEITA
class FotoReceita(models.Model):
    """Modelo para múltiplas fotos por receita"""
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='fotos_extras')
    foto = models.ImageField(upload_to='receitas/galeria/')
    legenda = models.CharField(max_length=200, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto Extra"
        verbose_name_plural = "Fotos Extras"
    
    def __str__(self):
        return f"Foto - {self.receita.titulo}"