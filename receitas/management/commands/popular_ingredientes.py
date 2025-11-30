from django.core.management.base import BaseCommand
from receitas.models import Ingrediente

class Command(BaseCommand):
    help = 'Popula o banco de dados com ingredientes comuns'

    def handle(self, *args, **kwargs):
        ingredientes_comuns = [
            # Cereais e Massas
            {'nome': 'Arroz branco', 'calorias_por_100g': 130, 'proteinas_por_100g': 2.7, 
             'carboidratos_por_100g': 28, 'gorduras_por_100g': 0.3, 'acucares_por_100g': 0.1, 'sodio_por_100g': 1},
            
            {'nome': 'Macarrão', 'calorias_por_100g': 371, 'proteinas_por_100g': 13, 
             'carboidratos_por_100g': 75, 'gorduras_por_100g': 1.5, 'acucares_por_100g': 2.7, 'sodio_por_100g': 6},
            
            {'nome': 'Farinha de trigo', 'calorias_por_100g': 364, 'proteinas_por_100g': 10, 
             'carboidratos_por_100g': 76, 'gorduras_por_100g': 1, 'acucares_por_100g': 0.3, 'sodio_por_100g': 2},
            
            # Proteínas
            {'nome': 'Frango (peito)', 'calorias_por_100g': 165, 'proteinas_por_100g': 31, 
             'carboidratos_por_100g': 0, 'gorduras_por_100g': 3.6, 'acucares_por_100g': 0, 'sodio_por_100g': 74},
            
            {'nome': 'Carne bovina (patinho)', 'calorias_por_100g': 143, 'proteinas_por_100g': 23, 
             'carboidratos_por_100g': 0, 'gorduras_por_100g': 5, 'acucares_por_100g': 0, 'sodio_por_100g': 60},
            
            {'nome': 'Ovo', 'calorias_por_100g': 155, 'proteinas_por_100g': 13, 
             'carboidratos_por_100g': 1.1, 'gorduras_por_100g': 11, 'acucares_por_100g': 1.1, 'sodio_por_100g': 124},
            
            {'nome': 'Peixe (tilápia)', 'calorias_por_100g': 96, 'proteinas_por_100g': 20, 
             'carboidratos_por_100g': 0, 'gorduras_por_100g': 1.7, 'acucares_por_100g': 0, 'sodio_por_100g': 52},
            
            # Laticínios
            {'nome': 'Leite integral', 'calorias_por_100g': 61, 'proteinas_por_100g': 3.2, 
             'carboidratos_por_100g': 4.8, 'gorduras_por_100g': 3.3, 'acucares_por_100g': 5.1, 'sodio_por_100g': 43},
            
            {'nome': 'Queijo mussarela', 'calorias_por_100g': 280, 'proteinas_por_100g': 19, 
             'carboidratos_por_100g': 3.1, 'gorduras_por_100g': 21, 'acucares_por_100g': 1.2, 'sodio_por_100g': 373},
            
            {'nome': 'Iogurte natural', 'calorias_por_100g': 61, 'proteinas_por_100g': 3.5, 
             'carboidratos_por_100g': 4.7, 'gorduras_por_100g': 3.3, 'acucares_por_100g': 4.7, 'sodio_por_100g': 46},
            
            # Vegetais
            {'nome': 'Tomate', 'calorias_por_100g': 18, 'proteinas_por_100g': 0.9, 
             'carboidratos_por_100g': 3.9, 'gorduras_por_100g': 0.2, 'acucares_por_100g': 2.6, 'sodio_por_100g': 5},
            
            {'nome': 'Cebola', 'calorias_por_100g': 40, 'proteinas_por_100g': 1.1, 
             'carboidratos_por_100g': 9.3, 'gorduras_por_100g': 0.1, 'acucares_por_100g': 4.2, 'sodio_por_100g': 4},
            
            {'nome': 'Alho', 'calorias_por_100g': 149, 'proteinas_por_100g': 6.4, 
             'carboidratos_por_100g': 33, 'gorduras_por_100g': 0.5, 'acucares_por_100g': 1, 'sodio_por_100g': 17},
            
            {'nome': 'Batata', 'calorias_por_100g': 77, 'proteinas_por_100g': 2, 
             'carboidratos_por_100g': 17, 'gorduras_por_100g': 0.1, 'acucares_por_100g': 0.8, 'sodio_por_100g': 6},
            
            {'nome': 'Cenoura', 'calorias_por_100g': 41, 'proteinas_por_100g': 0.9, 
             'carboidratos_por_100g': 10, 'gorduras_por_100g': 0.2, 'acucares_por_100g': 4.7, 'sodio_por_100g': 69},
            
            # Temperos e Condimentos
            {'nome': 'Azeite de oliva', 'calorias_por_100g': 884, 'proteinas_por_100g': 0, 
             'carboidratos_por_100g': 0, 'gorduras_por_100g': 100, 'acucares_por_100g': 0, 'sodio_por_100g': 2},
            
            {'nome': 'Sal', 'calorias_por_100g': 0, 'proteinas_por_100g': 0, 
             'carboidratos_por_100g': 0, 'gorduras_por_100g': 0, 'acucares_por_100g': 0, 'sodio_por_100g': 38758},
            
            {'nome': 'Açúcar', 'calorias_por_100g': 387, 'proteinas_por_100g': 0, 
             'carboidratos_por_100g': 100, 'gorduras_por_100g': 0, 'acucares_por_100g': 100, 'sodio_por_100g': 1},
            
            {'nome': 'Manteiga', 'calorias_por_100g': 717, 'proteinas_por_100g': 0.9, 
             'carboidratos_por_100g': 0.1, 'gorduras_por_100g': 81, 'acucares_por_100g': 0.1, 'sodio_por_100g': 11},
            
            # Leguminosas
            {'nome': 'Feijão preto', 'calorias_por_100g': 77, 'proteinas_por_100g': 4.5, 
             'carboidratos_por_100g': 14, 'gorduras_por_100g': 0.5, 'acucares_por_100g': 0.3, 'sodio_por_100g': 2},
            
            # Frutas
            {'nome': 'Banana', 'calorias_por_100g': 89, 'proteinas_por_100g': 1.1, 
             'carboidratos_por_100g': 23, 'gorduras_por_100g': 0.3, 'acucares_por_100g': 12, 'sodio_por_100g': 1},
            
            {'nome': 'Maçã', 'calorias_por_100g': 52, 'proteinas_por_100g': 0.3, 
             'carboidratos_por_100g': 14, 'gorduras_por_100g': 0.2, 'acucares_por_100g': 10, 'sodio_por_100g': 1},
        ]

        contador = 0
        for ing_data in ingredientes_comuns:
            ingrediente, created = Ingrediente.objects.get_or_create(
                nome=ing_data['nome'],
                defaults=ing_data
            )
            if created:
                contador += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Criado: {ingrediente.nome}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Já existe: {ingrediente.nome}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Total de ingredientes criados: {contador}')
        )
# Executar: python manage.py popular_ingredientes