from django.core.management.base import BaseCommand
from receitas.models import Categoria

class Command(BaseCommand):
    help = 'Popula categorias de receitas'

    def handle(self, *args, **kwargs):
        categorias = [
            {'nome': 'Café da Manhã', 'icone': 'bi-sun', 'cor': 'warning'},
            {'nome': 'Almoço', 'icone': 'bi-sunset', 'cor': 'primary'},
            {'nome': 'Jantar', 'icone': 'bi-moon-stars', 'cor': 'dark'},
            {'nome': 'Sobremesas', 'icone': 'bi-cake2', 'cor': 'danger'},
            {'nome': 'Lanches', 'icone': 'bi-cup-hot', 'cor': 'info'},
            {'nome': 'Bebidas', 'icone': 'bi-cup-straw', 'cor': 'success'},
            {'nome': 'Vegetariano', 'icone': 'bi-flower1', 'cor': 'success'},
            {'nome': 'Vegano', 'icone': 'bi-heart-pulse', 'cor': 'success'},
            {'nome': 'Fit/Saudável', 'icone': 'bi-heart', 'cor': 'danger'},
            {'nome': 'Massas', 'icone': 'bi-egg-fried', 'cor': 'warning'},
            {'nome': 'Carnes', 'icone': 'bi-basket', 'cor': 'danger'},
            {'nome': 'Peixes', 'icone': 'bi-water', 'cor': 'info'},
            {'nome': 'Saladas', 'icone': 'bi-tree', 'cor': 'success'},
            {'nome': 'Sopas', 'icone': 'bi-cup-hot', 'cor': 'warning'},
        ]

        for cat_data in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Criada: {categoria.nome}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Já existe: {categoria.nome}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Categorias populadas!'))

# Executar: python manage.py popular_categorias