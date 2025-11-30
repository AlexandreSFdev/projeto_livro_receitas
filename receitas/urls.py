from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_receitas, name='lista_receitas'),
    path('receita/<int:pk>/', views.detalhe_receita, name='detalhe_receita'),
    path('receita/nova/', views.criar_receita, name='criar_receita'),
    path('receita/<int:pk>/editar/', views.editar_receita, name='editar_receita'),
    path('receita/<int:pk>/deletar/', views.deletar_receita, name='deletar_receita'),
    path('minhas-receitas/', views.minhas_receitas, name='minhas_receitas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    # Favoritos
    path('receita/<int:pk>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    path('favoritas/', views.receitas_favoritas, name='receitas_favoritas'),
    
    # Categorias
    path('categorias/', views.todas_categorias, name='todas_categorias'),
    path('categoria/<int:categoria_id>/', views.receitas_por_categoria, name='receitas_por_categoria'),
    
    # Comentários
    path('receita/<int:pk>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
    
    # Populares
    path('populares/', views.receitas_populares, name='receitas_populares'),
]
