from django import forms
from django.forms import inlineformset_factory
from .models import Receita, IngredienteReceita, Ingrediente

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['titulo', 'descricao', 'modo_preparo', 'tempo_preparo', 
                  'porcoes', 'dificuldade', 'foto', 'categorias']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Descreva sua receita...'
            }),
            'modo_preparo': forms.Textarea(attrs={
                'rows': 8,
                'class': 'form-control',
                'placeholder': 'Passo a passo do preparo...'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bolo de Chocolate'
            }),
            'tempo_preparo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': '30'
            }),
            'porcoes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': '4'
            }),
            'dificuldade': forms.Select(attrs={
                'class': 'form-control'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'categorias': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }


class IngredienteReceitaForm(forms.ModelForm):
    # Campo para criar novo ingrediente
    novo_ingrediente = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o nome de um novo ingrediente...',
            'class': 'form-control'
        }),
        label='Novo ingrediente'
    )
    
    class Meta:
        model = IngredienteReceita
        fields = ['ingrediente', 'quantidade', 'unidade', 'observacao']
        widgets = {
            'ingrediente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '100'
            }),
            'unidade': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: picado, ralado...'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        ingrediente = cleaned_data.get('ingrediente')
        novo_ingrediente = cleaned_data.get('novo_ingrediente')
        
        # Se digitou novo ingrediente e não selecionou da lista
        if novo_ingrediente and not ingrediente:
            # Criar ou buscar ingrediente
            ingrediente_obj, created = Ingrediente.objects.get_or_create(
                nome=novo_ingrediente.strip()
            )
            cleaned_data['ingrediente'] = ingrediente_obj
            
            if created:
                # Ingrediente criado sem dados nutricionais
                # Você pode adicionar uma mensagem informando isso
                pass
        
        return cleaned_data


IngredienteReceitaFormSet = inlineformset_factory(
    Receita,
    IngredienteReceita,
    form=IngredienteReceitaForm,
    fields=['ingrediente', 'quantidade', 'unidade', 'observacao'],
    extra=5,  # Formulários extras vazios
    can_delete=True,
    min_num=1,  # Mínimo de 1 ingrediente
    validate_min=True,
)